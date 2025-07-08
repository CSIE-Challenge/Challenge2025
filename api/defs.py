from enum import IntEnum, auto


class CommandType(IntEnum):
    GET_ALL_TERRAIN = 1
    GET_SCORES = 2
    GET_CURRENT_WAVE = 3
    GET_REMAIN_TIME = 4
    GET_TIME_UNTIL_NEXT_WAVE = 5
    GET_MONEY = 6
    GET_INCOME = 7
    PLACE_TOWER = 101
    GET_ALL_TOWERS = 102
    GET_TOWER = 103
    SPAWN_ENEMY = 201
    GET_ENEMY_COOLDOWN = 202
    GET_ALL_ENEMY_INFO = 203
    GET_AVAILABLE_ENEMIES = 204
    GET_CLOSEST_ENEMIES = 205
    GET_ENEMIES_IN_RANGE = 206
    CAST_SPELL = 301
    GET_SPELL_COOLDOWN = 302
    GET_ALL_SPELL_COST = 303
    GET_EFFECTIVE_SPELLS = 304
    SEND_CHAT = 401
    GET_CHAT_HISTORY = 402


class TerrainType(IntEnum):
    OUT_OF_BOUNDS = 0
    EMPTY = 1
    ROAD = 2
    OBSTACLE = 3


class TowerType(IntEnum):
    BASIC = auto()


class EnemyType(IntEnum):
    BASIC = auto()


class SpellType(IntEnum):
    POISON = auto()
    DOUBLE_INCOME = auto()
    TELEPORT = auto()


class StatusCode(IntEnum):
    OK = 200
    ILLFORMED_COMMAND = 400
    AUTH_FAIL = 401
    ILLEGAL_ARGUMENT = 402
    COMMAND_ERR = 403
    NOT_FOUND = 404
    TOO_FREQUENT = 405
    INTERNAL_ERR = 500
    CLIENT_ERR = 501


class TypeCode(IntEnum):
    NULL_TYPE = 0
    BOOL_TYPE = 1
    INT_TYPE = 2
    STRING_TYPE = 4
    VECTOR2I_TYPE = 6
    DICTIONARY_TYPE = 27
    LIST_TYPE = 28


class Vector2:
    def __init__(self, _x: int | None, _y: int | None) -> None:
        self.x = _x if _x is not None else 0
        self.y = _y if _y is not None else 0

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class ApiException(Exception):
    def __init__(self, source_fn: CommandType, code: StatusCode, what: str) -> None:
        super().__init__(
            f"API call {source_fn.name}({source_fn.value}) fails with status code {code.name}({code.value}): {what}")
        self.source_fn = source_fn
        self.code = code
        self.what = what
