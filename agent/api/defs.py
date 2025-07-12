from __future__ import annotations
from enum import IntEnum, auto

class CommandType(IntEnum):
    GET_ALL_TERRAIN = 1
    GET_SCORES = 2
    GET_CURRENT_WAVE = 3
    GET_REMAIN_TIME = 4
    GET_TIME_UNTIL_NEXT_WAVE = 5
    GET_MONEY = 6
    GET_INCOME = 7
    GET_GAME_STATUS = 8
    GET_TERRAIN = 9
    PLACE_TOWER = 101
    GET_ALL_TOWERS = 102
    GET_TOWER = 103
    SPAWN_UNIT = 201
    GET_AVAILABLE_UNITS = 202
    GET_ALL_ENEMIES = 203
    CAST_SPELL = 301
    GET_SPELL_COOLDOWN = 302
    GET_SPELL_COST = 303
    GET_EFFECTIVE_SPELLS = 304
    SEND_CHAT = 401
    GET_CHAT_HISTORY = 402
    SET_CHAT_NAME_COLOR = 403
    PIXELCAT = 501
    GET_DEVS = 502
    SET_NAME = 503


class TerrainType(IntEnum):
    OUT_OF_BOUNDS = 0
    EMPTY = 1
    ROAD = 2
    OBSTACLE = 3


class TowerType(IntEnum):
    NONE = 0
    FIRE_MARIO = 1
    ICE_LUIGI = 2
    DONEKEY_KONG = 3
    FORT = 4
    SHY_GUY = 5


class EnemyType(IntEnum):
    BUZZY_BEETLE = 0
    GOOMBA = 1
    KOOPA_JR = 2
    KOOPA_PARATROOPA = 3
    KOOPA = 4
    SPINY_SHELL = 5
    WIGGLER = 6


class SpellType(IntEnum):
    POISON = 1
    DOUBLE_INCOME = 2
    TELEPORT = 3


class StatusCode(IntEnum):
    OK = 200
    ILLFORMED_COMMAND = 400
    AUTH_FAIL = 401
    ILLEGAL_ARGUMENT = 402
    COMMAND_ERR = 403
    NOT_FOUND = 404
    TOO_FREQUENT = 405
    NOT_STARTED = 406
    INTERNAL_ERR = 500
    CLIENT_ERR = 501


class TypeCode(IntEnum):
    NULL_TYPE = 0
    BOOL_TYPE = 1
    INT_TYPE = 2
    FLOAT_TYPE = 3
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


class Tower:
    def __init__(self, _type: TowerType, position: Vector2, level_a: int, level_b: int, aim: bool = True, 
                 anti_air: bool = False, bullet_number: int = 1, reload: int = 60, 
                 range: int = 100, damage: int = 10, bullet_effect: str = 'none') -> None:
        self.type = _type
        self.position = position
        self.level_a = level_a
        self.level_b = level_b
        self.aim = aim
        self.anti_air = anti_air
        self.bullet_number = bullet_number
        self.reload = reload
        self.range = range
        self.damage = damage
        self.bullet_effect = bullet_effect

    @classmethod
    def from_dict(cls, data: dict) -> 'Tower' | None:
        if not data:
            return None
        return cls(
            _type=TowerType(data['type']),
            position=Vector2(data['position']['x'], data['position']['y']),
            level_a=data['level_a'],
            level_b=data['level_b'],
            aim=data.get('aim'),
            anti_air=data.get('anti_air'),
            bullet_number=data.get('bullet_number'),
            reload=data.get('reload'),
            range=data.get('range'),
            damage=data.get('damage'),
            bullet_effect=data.get('bullet_effect', 'none')
        )

    def __str__(self) -> str:
        return f"Tower(type={self.type.name}, position={self.position}, level_a={self.level_a}, level_b={self.level_b})"

    def __repr__(self) -> str:
        return self.__str__()


class Enemy:
    def __init__(self, type: EnemyType, position: Vector2, progress_ratio: float, deploy_cost: int, health: int, max_health: int,
                 flying: bool, damage: int, max_speed: int, knockback_resist: bool, kill_reward: int,
                 income_impact: int, cool_down: int = None) -> None:
        self.type = type
        self.position = position
        self.progress_ratio = progress_ratio
        self.deploy_cost = deploy_cost
        self.health = health
        self.max_health = max_health
        self.flying = flying
        self.damage = damage
        self.max_speed = max_speed
        self.knockback_resist = knockback_resist
        self.kill_reward = kill_reward
        self.income_impact = income_impact
        self.cool_down = cool_down

    @classmethod
    def from_dict(cls, data: dict) -> 'Enemy':
        return cls(
            type=EnemyType(data['type']),
            position=Vector2(data['position']['x'], data['position']['y']),
            progress_ratio=data.get('progress_ratio'),
            deploy_cost=data.get('deploy_cost'),
            income_impact=data.get('income_impact'),
            health=data.get('health'),
            max_health=data.get('max_health'),
            damage=data.get('damage'),
            max_speed=data.get('max_speed'),
            flying=data.get('flying'),
            knockback_resist=data.get('knockback_resist'),
            kill_reward=data.get('kill_reward'),
            cool_down=data.get('cool_down', 'none')
        )

    def __str__(self) -> str:
        return f"Enemy(type={self.type.name}, position={self.position}, progress ratio={self.progress_ratio}, health={self.health}/{self.max_health})"

    def __repr__(self) -> str:
        return self.__str__()

