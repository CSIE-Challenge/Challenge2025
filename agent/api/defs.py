from __future__ import annotations
from enum import IntEnum, auto

class CommandType(IntEnum):
    """每種API對應的編號，用於報錯訊息。"""

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
    PIXELCAT = 501
    GET_DEVS = 502


class GameStatus(IntEnum):
    """遊戲運行狀態。"""

    PREPARING = 0
    """遊戲尚未開始，正在準備中。"""

    RUNNING = 1
    """遊戲已經開始且正在進行中。"""

    PAUSED = 2
    """遊戲已經開始，但暫時被暫停中。"""



class TerrainType(IntEnum):
    """地圖地形。"""

    OUT_OF_BOUNDS = 0
    """超出邊界的區域。"""

    EMPTY = 1
    """空地，可放置塔。"""

    ROAD = 2
    """道路，是敵人行進的路徑，不可以放置塔。"""

    OBSTACLE = 3
    """障礙物，不可行走也不能放塔。"""


class TowerType(IntEnum):
    """塔的種類。"""
    
    FIRE_MARIO = 1
    """
    火焰馬利歐，攻速快、範圍廣、可以瞄準飛行單位。  
    升級可選擇增加攻速、範圍、傷害或增加燃燒效果。
    """

    ICE_LUIGI = 2
    """
    寒冰路易吉，攻擊附帶範圍緩速效果。  
    升級可選擇增加攻速、範圍、傷害或改為範圍攻擊。
    """

    DONEKEY_KONG = 3
    """
    森喜剛，原地範圍攻擊（以自身為中心的圓）。  
    升級可選擇擊退效果或瞄準直線攻擊。
    """
    
    FORT = 4
    """
    砲台，沿直線發射炮彈刺客。（穿透敵人）。  
    升級可選擇提高傷害並不穿透(碰到敵人即爆炸)或制空能力。
    """
    
    SHY_GUY = 5
    """
    嘿呵：分散投擲多把飛刀、可以瞄準飛行單位。  
    升級可選擇增加攻速、範圍、傷害、飛刀數量或改為投擲迴旋鏢。
    """


class EnemyType(IntEnum):
    """敵人種類。"""

    BUZZY_BEETLE = 0
    """鋼盔龜。"""

    GOOMBA = 1
    """栗寶寶。"""

    KOOPA_JR = 2
    """庫巴 Jr."""

    KOOPA_PARATROOPA = 3
    """飛行龜。"""

    KOOPA = 4
    """庫巴。"""
    
    SPINY_SHELL = 5
    """龜殼。"""
    
    WIGGLER = 6
    """花毛毛。"""

class SpellType(IntEnum):
    """技能類別。"""

    POISON = 1
    """毒藥，對範圍內的敵人造成持續傷害。"""

    DOUBLE_INCOME = 2
    """一段時間內收到的金錢變兩倍。"""

    TELEPORT = 3
    """傳送我方地圖中一個區域的所有敵人到對手的場地內，重新從起點開始走。"""


class StatusCode(IntEnum):
    """呼叫API得到的回覆狀態。"""

    OK = 200
    """成功。"""

    ILLFORMED_COMMAND = 400
    """
    呼叫API的參數陣列不符格式。  
    ex: 參數數量錯誤。
    """

    AUTH_FAIL = 401
    """認證失敗。"""

    ILLEGAL_ARGUMENT = 402
    """API傳入參數型別錯誤。"""

    COMMAND_ERR = 403
    """指令施放失敗。"""

    NOT_FOUND = 404
    """CommandType不存在。"""

    TOO_FREQUENT = 405
    """最近兩次的API請求相隔時間過短。"""

    NOT_STARTED = 406
    """遊戲尚未開始。"""
    
    INTERNAL_ERR = 500
    """Godot server端出現問題（請向開發組反映，對不起！！！）。"""

    CLIENT_ERR = 501
    """Python client端出現問題（請向開發組反映，對不起！！！）。"""


class TypeCode(IntEnum):
    """基本型別代號。"""

    NULL_TYPE = 0
    """空值。"""

    BOOL_TYPE = 1
    """布林。"""
    
    INT_TYPE = 2
    """整數。"""
    
    FLOAT_TYPE = 3
    """浮點數。"""

    STRING_TYPE = 4
    """字串。"""

    VECTOR2I_TYPE = 6
    """二維向量。"""

    DICTIONARY_TYPE = 27
    """字典。"""

    LIST_TYPE = 28
    """串列。"""


class Vector2:
    """二維向量。"""

    def __init__(self, _x: int | None, _y: int | None) -> None:
        self.x = _x if _x is not None else 0
        """x座標，若傳None則設為0。"""

        self.y = _y if _y is not None else 0
        """y座標，若傳None則設為0。"""

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class ApiException(Exception):
    """API請求的錯誤訊息。"""

    def __init__(self, source_fn: CommandType, code: StatusCode, what: str) -> None:
        super().__init__(
            f"API call {source_fn.name}({source_fn.value}) fails with status code {code.name}({code.value}): {what}")
        self.source_fn = source_fn
        """見class CommandType。"""

        self.code = code
        """見class StatusCode。"""

        self.what = what
        """完整錯誤訊息內容。"""


class Tower:
    """防禦塔。"""
    
    def __init__(self, _type: TowerType, position: Vector2, level_a: int, level_b: int, aim: bool = True, 
                 anti_air: bool = False, bullet_number: int = 1, reload: int = 60, 
                 range: int = 100, damage: int = 10, bullet_effect: str = 'none') -> None:
        self.type = _type
        """塔的型別，見class TowerType"""

        self.position = position
        """塔的座標，地圖左上角為(0, 0)。"""

        self.level_a = level_a
        """塔的等級分支一。"""

        self.level_b = level_b
        """
        塔的等級分支二。  
        (level_a, level_b) =
        - (1, 1): 1
        - (2, 1): 2a
        - (1, 2): 2b
        - (3, 1): 3a
        - (1, 3): 3b
        """

        self.aim = aim
        """是否能瞄準敵人。"""

        self.anti_air = anti_air
        """是否能攻擊空中單位。"""

        self.bullet_number = bullet_number
        """每次攻擊的子彈數量。"""

        self.reload = reload
        """每分鐘攻擊次數。"""

        self.range = range
        """瞄準範圍半徑。"""

        self.damage = damage
        """攻擊傷害。"""

        self.bullet_effect = bullet_effect
        """
        特殊效果。
        - none: 無
        - fire: 燃燒的持續傷害
        - freeze: 緩速
        - deep_freeze: 強化緩速
        - knockback: 擊退 knockback_resist = False 的敵人
        - far_knockback: 擊退所有敵人
        """

    @classmethod
    def from_dict(cls, data: dict) -> 'Tower | None':
        if not data:
            return None
        return cls(
            _type=TowerType(data['type']),
            position=Vector2(data['position']['x'], data['position']['y']),
            level_a=data['level_a'],
            level_b=data['level_b'],
            aim=data['aim'],
            anti_air=data['anti_air'],
            bullet_number=data['bullet_number'],
            reload=data['reload'],
            range=data['range'],
            damage=data['damage'],
            # bullet_effect=data['bullet_effect'],
        )

    def __str__(self) -> str:
        return f"Tower(type={self.type.name}, position={self.position}, level_a={self.level_a}, level_b={self.level_b})"

    def __repr__(self) -> str:
        return self.__str__()


class Enemy:
    """敵人。"""
    
    def __init__(self, type: EnemyType, position: Vector2, progress_ratio: float, deploy_cost: int, health: int, max_health: int,
                 flying: bool, damage: int, max_speed: int, knockback_resist: bool, kill_reward: int,
                 income_impact: int, cool_down: int = None) -> None:
        self.type = type
        """敵人型別。"""

        self.position = position
        """敵人位置。"""
        
        self.progress_ratio = progress_ratio
        """敵人走完的路程比例。"""

        self.deploy_cost = deploy_cost
        """派遣敵人對持有金幣的影響。"""

        self.health = health
        """敵人當前生命值。"""
        
        self.max_health = max_health
        """敵人最大生命值。"""

        self.flying = flying
        """是不是空中單位。"""

        self.damage = damage
        """對塔能造成的傷害。"""

        self.max_speed = max_speed
        """最高速度。"""

        self.knockback_resist = knockback_resist
        """擊退抵抗，若為true則不會被擊退。"""

        self.kill_reward = kill_reward
        """擊殺該敵人會獲得的獎勵。"""

        self.income_impact = income_impact
        """派兵到對手場地後對 income 的影響，可正可負。"""

        self.cool_down = cool_down
        """派兵時間間隔。"""


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

