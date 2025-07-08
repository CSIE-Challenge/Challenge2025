import asyncio
import re
import time
from typing import Any, Callable, cast

from api.defs import *
from api.serialization import *
from api.utils import *
from api.logger import logger
from websockets.asyncio.client import connect


class GameClientBase:

    COMMAND_RATE_LIMIT_MSEC = 10

    def __init__(
            self,
            port: int,
            token: str | None = None,
            server_domain: str = "localhost",
            command_timeout_msec: int = 20,
            retry_count: int = 3) -> None:

        if token is None:
            token = input("Enter the token required for connection: ")

        enforce_type('port', port, int)
        enforce_condition('0 <= port < 65536',
                          port, lambda p: 0 <= p < 65536)
        enforce_type('token', token, str)
        enforce_condition('token must be a 8-digit hexadecimal number',
                          token, lambda t: re.fullmatch(r'[0-9a-fA-F]{8}', t))
        enforce_type('server_domain', server_domain, str)
        enforce_type('command_timeout_msec', command_timeout_msec, int)
        enforce_condition(f'command_timeout_msec must not be at least {self.COMMAND_RATE_LIMIT_MSEC} ms',
                          command_timeout_msec, lambda x: x >= self.COMMAND_RATE_LIMIT_MSEC)
        enforce_type('retry_count', retry_count, int)
        enforce_condition('retry_count must be positive', retry_count, lambda x: x > 0)

        self.port = port
        self.token = token.lower()
        self.server_domain = server_domain
        self.command_timeout_msec = command_timeout_msec
        self.retry_count = retry_count

        self.last_command = time.time_ns()
        self.server_url = f"ws://{self.server_domain}:{self.port}"
        asyncio.get_event_loop().run_until_complete(self.__ws_connect())
        logger.info(f"connected to {self.server_url}")

    async def __ws_connect(self) -> None:
        self.ws = await connect(self.server_url)
        authed = await self.__ws_authenticate()
        if not authed:
            raise ConnectionError("authentication failed. Is the provided token correct?")
        # no need to disconnect by ws.close(); the socket is automatically disconnected on program exit

    async def __ws_authenticate(self) -> bool:
        try:
            await self.ws.send(self.token)
            response = await self.ws.recv()
        except Exception:
            raise ConnectionError("authentication failed due to connection error")
        return response == "Connection OK. Have Fun!"  # magic string from game server

    async def __ws_send_gdvars(self, deserialized: Any) -> None:
        serialized = var_to_bytes(deserialized)
        await self.ws.send(serialized)

    async def __ws_recv_gdvars(self) -> Any:
        recved = await self.ws.recv()
        enforce_type('serialized byte sequence received', recved, bytes)
        serialized: bytes = cast(bytes, recved)
        deserialized = bytes_to_var(serialized)
        return deserialized

    async def __send_command(self, command_id, args) -> Any:
        time_to_wait = self.COMMAND_RATE_LIMIT_MSEC * 1_000_000 - (time.time_ns() - self.last_command)
        if time_to_wait >= 0:
            await asyncio.sleep(time_to_wait / (10 ** 9))
        args = [int(command_id), *args]
        async def send_and_receive():
            await self.__ws_send_gdvars(args)
            self.last_command = time.time_ns()
            return await self.__ws_recv_gdvars()
        return await asyncio.wait_for(send_and_receive(), timeout=(self.command_timeout_msec / 1000))

    def __check_arg_types(self, source_fn: CommandType, arg_types: list[type], args: list[Any]) -> bool:
        if len(arg_types) != len(args):
            raise ApiException(source_fn, StatusCode.ILLFORMED_COMMAND, f"{source_fn} expected {len(arg_types)} arguments, got {len(args)}")
        else:
            for i in range(len(arg_types)):
                if not isinstance(args[i], arg_types[i]):
                    raise ApiException(source_fn, StatusCode.ILLEGAL_ARGUMENT, f"type mismatch at argument {i} of {source_fn}")
        return True

    def __check_status_code(self, source_fn: CommandType, ret: Any) -> Any:
        if not isinstance(ret, list):
            raise ApiException(source_fn, StatusCode.INTERNAL_ERR,
                               f"object received from the game was not an array")
        if len(ret) < 1:
            raise ApiException(source_fn, StatusCode.INTERNAL_ERR,
                               f"did not receive a status code")
        statuscode = ret[0]
        if statuscode not in StatusCode:
            raise ApiException(source_fn, StatusCode.INTERNAL_ERR,
                               f"unknown status code {statuscode} from the server")
        statuscode = StatusCode(statuscode)
        if statuscode != StatusCode.OK:
            if len(ret) == 2 and isinstance(ret[1], str) and len(ret[1]) != 0:
                raise ApiException(source_fn, statuscode, ret[1])
            raise ApiException(source_fn, statuscode,
                               f"(empty or corrupted error message)")
        match len(ret):
            case 1:
                return None
            case 2:
                return ret[1]
            case _:
                return ret[1:]

    def __cast_return_type(self, source_fn: CommandType, inner_ret_type: type | None, ret: Any) -> Any:
        if inner_ret_type is None:
            if ret is None:
                return ret
            else:
                raise ApiException(
                    source_fn, StatusCode.INTERNAL_ERR, f"unexpected return value")
        if isinstance(ret, list):
            for i in range(len(ret)):
                ret[i] = self.__cast_return_type(
                    source_fn, inner_ret_type, ret[i])
            return ret
        elif isinstance(ret, inner_ret_type):
            return ret
        try:
            return inner_ret_type(ret)
        except:
            raise ApiException(source_fn, StatusCode.CLIENT_ERR,
                               f"failed to cast return type from {type(ret)} to {inner_ret_type}")

    def await_send_command(self, command_id: CommandType, args: list[Any], arg_types: list[type], inner_ret_type: type | None) -> Any:
        retry_count = self.retry_count
        while retry_count > 0:
            try:
                self.__check_arg_types(command_id, arg_types, list(args))
                fut = self.__send_command(command_id, args)
                ret = asyncio.get_event_loop().run_until_complete(fut)
                value = self.__check_status_code(command_id, ret)
                value = self.__cast_return_type(command_id, inner_ret_type, value)
                return value
            except TimeoutError:
                retry_count -= 1
                logger.warning(f"command {command_id.name} timed out, retrying")
            except ApiException as e:
                if e.code == StatusCode.TOO_FREQUENT:
                    continue
                else:
                    return e
            except Exception as e:
                raise ApiException(command_id, StatusCode.CLIENT_ERR, f"unexpected error\nwhat: {e}")
        raise ApiException(command_id, StatusCode.CLIENT_ERR, f"command {command_id.name} timed out, retry limit {self.retry_count} exceeded")


# decorator for command handlers
# the decorated function itself is just a dummy function that never gets called
def game_command(command_id: CommandType, arg_types: list[type], inner_ret_type: type | None) -> Callable:
    def decorator(_: Callable) -> Callable:
        def wrapped(client: GameClientBase, *args) -> Any:
            return client.await_send_command(command_id, list(args), arg_types, inner_ret_type)
        return wrapped
    return decorator
