from asyncio import TimeoutError, get_event_loop, wait_for
import re
from typing import Any, Callable, cast

from api.defs import *
from api.serialization import *
from api.utils import *
from websockets.asyncio.client import connect


class GameClientBase:

    def __init__(
            self,
            port: int,
            token: str | None = None,
            server_domain: str = "localhost",
            retry_interval_msec: int = 30,
            retry_count: int = 3) -> None:

        if token is None:
            token = input("[API] Enter the token required for connection: ")

        enforce_type('port', port, int)
        enforce_condition('0 <= port < 65536',
                          port, lambda p: 0 <= p < 65536)
        enforce_type('token', token, str)
        enforce_condition('token must be a 8-digit hexadecimal number',
                          token, lambda t: re.fullmatch(r'[0-9a-fA-F]{8}', t))
        enforce_type('server_domain', server_domain, str)
        enforce_type('retry_interval_msec', retry_interval_msec, int)
        enforce_condition('retry_interval_msec must not be at least 10 msec',
                          retry_interval_msec, lambda x: x >= 10)
        enforce_type('retry_count', retry_count, int)
        enforce_condition('retry_count must be positive',
                          retry_count, lambda x: x > 0)
        self.port = port
        self.token = token.lower()
        self.server_domain = server_domain
        self.retry_interval_msec = retry_interval_msec
        self.retry_count = retry_count
        self.server_url = f"ws://{self.server_domain}:{self.port}"
        get_event_loop().run_until_complete(self.__ws_connect())
        print(f"[API] Info: connected to {self.server_url}")

    async def __ws_connect(self) -> None:
        self.ws = await connect(self.server_url)
        authed = await self.__ws_authenticate()
        if not authed:
            print("[API] Error: failed authenticating. Is the provided token correct?")
            raise ConnectionError()
        # no need to disconnect by ws.close(); the socket is automatically disconnected on program exit

    async def __ws_authenticate(self) -> bool:
        try:
            await self.__ws_send(self.token)
            response = await self.__ws_recv()
        except Exception as e:
            print("[API] Error: connection error during authentication")
            raise e
        return response == "Connection OK. Have Fun!"  # magic string from game server

    async def __ws_send(self, msg: str | bytes) -> None:
        try:
            await wait_for(self.ws.send(msg), timeout=(self.retry_interval_msec / 1000))
        except TimeoutError:
            print("[API] Error: sending message timed out")
            raise TimeoutError()

    async def __ws_recv(self) -> str | bytes:
        received = False
        msg = ""  # surpass unbound type checking
        for _ in range(self.retry_count):
            try:
                msg = await wait_for(self.ws.recv(), timeout=(self.retry_interval_msec / 1000))
                received = True
            except TimeoutError:
                print("[API] Warning: receiving message timed out, retrying")
        if not received:
            print("[API] Error: receiving message timed out, retrying limit exceeded")
            raise TimeoutError()
        return msg

    async def __ws_send_gdvars(self, deserialized: Any) -> None:
        try:
            serialized = var_to_bytes(deserialized)
        except Exception as e:
            print("[API] Error: failed serializing an object into byte sequence")
            raise e
        await self.__ws_send(serialized)

    async def __ws_recv_gdvars(self) -> Any:
        recved = await self.__ws_recv()
        enforce_type('serialized byte sequence received', recved, bytes)
        serialized: bytes = cast(bytes, recved)
        try:
            deserialized = bytes_to_var(serialized)
        except Exception as e:
            print(
                "[API] Error: failed deserializing recieved byte sequence into an object")
            raise e
        return deserialized

    async def __send_command(self, command_id, args) -> Any:
        args = [int(command_id), *args]
        await self.__ws_send_gdvars(args)
        return await self.__ws_recv_gdvars()

    def __check_arg_types(self, source_fn: CommandType, arg_types: list[type], args: list[Any]) -> bool:
        matched = True
        if len(arg_types) != len(args):
            matched = False
            print(
                f"[API] Error: {source_fn} expected {len(arg_types)} arguments, got {len(args)}")
            raise RuntimeError
        else:
            for i in range(len(arg_types)):
                if not isinstance(args[i], arg_types[i]):
                    matched = False
                    print(
                        f"[API] Error: type mismatch at argument {i} of {source_fn}")
                    raise TypeError
        return matched

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
            raise ApiException(source_fn, StatusCode.INTERNAL_ERR,
                               f"failed to cast return type from {type(ret)} to {inner_ret_type}")

    def await_send_command(self, command_id: CommandType, args: list[Any], arg_types: list[type], inner_ret_type: type | None) -> Any:
        try:
            if not self.__check_arg_types(command_id, arg_types, list(args)):
                return [StatusCode.ILLEGAL_ARGUMENT]
            fut = self.__send_command(command_id, args)
            ret = get_event_loop().run_until_complete(fut)
            value = self.__check_status_code(command_id, ret)
            value = self.__cast_return_type(command_id, inner_ret_type, value)
        except ApiException as e:
            return e
        return value


# decorator for command handlers
# the decorated function itself is just a dummy function that never gets called
def game_command(command_id: CommandType, arg_types: list[type], inner_ret_type: type | None) -> Callable:
    def decorator(_: Callable) -> Callable:
        def wrapped(client: GameClientBase, *args) -> Any:
            return client.await_send_command(command_id, list(args), arg_types, inner_ret_type)
        return wrapped
    return decorator
