from asyncio import TimeoutError, get_event_loop, wait_for
import re
from typing import Any, Callable, TypeVar, cast

from api.gdtype.defs import *
from api.gdtype.serialization import *
from websockets.asyncio.client import connect


def enforce_type(name, obj, *args):
    if not isinstance(obj, args):
        types = " | ".join(list(map(lambda x: x.__name__, args)))
        raise TypeError(f"[API Server] Error: {name} must be type {types}")


def enforce_condition(condition_str, var, condition_fn):
    if not condition_fn(var):
        raise ValueError(f"[API Server] Error: condition violated: {condition_str}")


# declare TypeVar to avoid forward referencing
GameClientType = TypeVar("GameClientType", bound="GameClient")

def game_command(command_id: int, arg_types: list[type]) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapped(client: GameClientType, *args) -> Any:
            if client.check_arg_types(func.__name__, arg_types, list(args)):
                fut = client.send_command(command_id, args)
                return get_event_loop().run_until_complete(fut)
            return [StatusCode.ILLEGAL_ARGUMENT]
        return wrapped
    return decorator


class GameClient:

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
            print([int.from_bytes(serialized[i:i+4], "little") for i in range(0, len(serialized), 4)])
            deserialized = bytes_to_var(serialized)
            print(deserialized)
        except Exception as e:
            print(
                "[API] Error: failed deserializing recieved byte sequence into an object")
            raise e
        return deserialized

    async def send_command(self, command_id, args) -> Any:
        args = [int(command_id), *args]
        await self.__ws_send_gdvars(args)
        return await self.__ws_recv_gdvars()
    
    def check_arg_types(self, fn_name: str, arg_types: list[type], args: list[Any]) -> bool:
        matched = True
        if len(arg_types) != len(args):
            matched = False
            print(f"[API] Error: {fn_name} expected {len(arg_types)} arguments, got {len(args)}")
            raise RuntimeError
        else:
            for i in range(len(arg_types)):
                if not isinstance(args[i], arg_types[i]):
                    matched = False
                    print(f"[API] Error: type mismatch at argument {i} of {fn_name}")
                    raise TypeError
        return matched

    @game_command(CommandType.GET_ALL_TERRAIN, [])
    def get_all_terrain(self) -> list[list[TerrainType]]:
        raise NotImplementedError

    @game_command(CommandType.GET_SCORES, [bool])
    def get_scores(self, owned: bool) -> int:
        raise NotImplementedError
