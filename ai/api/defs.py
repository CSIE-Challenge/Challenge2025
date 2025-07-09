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
    SPAWN_ENEMY = 201
    GET_ENEMY_COOLDOWN = 202
    GET_ENEMY_INFO = 203
    GET_AVAILABLE_ENEMIES = 204
    GET_CLOSEST_ENEMIES = 205
    GET_ENEMIES_IN_RANGE = 206
    CAST_SPELL = 301
    GET_SPELL_COOLDOWN = 302
    GET_SPELL_COST = 303
    GET_EFFECTIVE_SPELLS = 304
    SEND_CHAT = 401
    GET_CHAT_HISTORY = 402
    PIXELCAT = 501
    GET_DEVS = 502


class TerrainType(IntEnum):
    OUT_OF_BOUNDS = 0
    EMPTY = 1
    ROAD = 2
    OBSTACLE = 3


class TowerType(IntEnum):
    BASIC = 0


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
    def __init__(self, _type: TowerType, position: Vector2, level: int, aim: bool = True, 
                 anti_air: bool = False, bullet_number: int = 1, reload: int = 60, 
                 range: int = 100, damage: int = 10, bullet_effect: str = 'none') -> None:
        self.type = _type
        self.position = position
        self.level = level
        self.aim = aim
        self.anti_air = anti_air
        self.bullet_number = bullet_number
        self.reload = reload
        self.range = range
        self.damage = damage
        self.bullet_effect = bullet_effect

    @classmethod
    def from_dict(cls, data: dict) -> 'Tower':
        return cls(
            _type=TowerType(data['type']),
            position=Vector2(data['position']['x'], data['position']['y']),
            level=data['level'],
            aim=data.get('aim'),
            anti_air=data.get('anti_air'),
            bullet_number=data.get('bullet_number'),
            reload=data.get('reload'),
            range=data.get('range'),
            damage=data.get('damage'),
            bullet_effect=data.get('bullet_effect', 'none')
        )

    def __str__(self) -> str:
        return f"Tower(type={self.type.name}, position={self.position}, level={self.level})"


class Enemy:
    def __init__(self, _type: EnemyType, position: Vector2, health: int, max_hp: int = None,
                 flying: bool = False, damage: int = None, armor: int = None, 
                 shield: int = None, knockback_resist: bool = False, kill_reward: int = None,
                 income_impact: int = None, cool_down: int = None) -> None:
        self.type = _type
        self.position = position
        self.health = health
        self.max_hp = max_hp
        self.flying = flying
        self.damage = damage
        self.armor = armor
        self.shield = shield
        self.knockback_resist = knockback_resist
        self.kill_reward = kill_reward
        self.income_impact = income_impact
        self.cool_down = cool_down

    @classmethod
    def from_dict(cls, data: dict) -> 'Enemy':
        return cls(
            _type=EnemyType(data['type']),
            position=Vector2(data['position']['x'], data['position']['y']),
            health=data['health'],
            max_hp=data.get('max_hp'),
            flying=data.get('flying'),
            damage=data.get('damage'),
            armor=data.get('armor'),
            shield=data.get('shield'),
            knockback_resist=data.get('knockback_resist'),
            kill_reward=data.get('kill_reward'),
            income_impact=data.get('income_impact'),
            cool_down=data.get('cool_down')
        )

    def __str__(self) -> str:
        return f"Enemy(type={self.type.name}, position={self.position}, health={self.health})"


class Spell:
    def __init__(self, _type: SpellType, position: Vector2, duration: int = 0, 
                 damage: int = 0, range: int = 0, multiplier: float = 1.0) -> None:
        self.type = _type
        self.position = position
        self.duration = duration
        self.damage = damage
        self.range = range
        self.multiplier = multiplier

    @classmethod
    def from_dict(cls, data: dict) -> 'Spell':
        return cls(
            _type=SpellType(data['type']),
            position=Vector2(data['position']),
            duration=data.get('duration'),
            damage=data.get('damage'),
            range=data.get('range'),
            multiplier=data.get('multiplier')
        )

    def __str__(self) -> str:
        return f"Spell(type={self.type.name}, position={self.position}, duration={self.duration})"
