# Temporarily written in a separate file to avoid merge conflict
# will be added into defs.py and game_client.py

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
    """地圖地形。"""

    OUT_OF_BOUNDS = 0
    """界外。"""

    EMPTY = 1
    """空地，可放置塔。"""

    ROAD = 2
    """道路，角色可行走。"""

    OBSTACLE = 3
    """障礙，不可行走也不能放塔。"""


class TowerType(IntEnum):
    """塔的種類。"""

    NONE = auto()
    """無屬性。"""

    FIRE_MARIO = auto()
    """
    火焰馬利歐，攻速快、範圍廣、可以瞄準飛行單位。  
    升級可選擇增加攻速、範圍、傷害或增加燃燒效果。
    """

    ICE_LUIGI = auto()
    """
    寒冰路易吉，攻擊附帶範圍緩速效果。  
    升級可選擇增加攻速、範圍、傷害或改為範圍攻擊。
    """

    DONEKEY_KONG = auto()
    """
    森喜剛，原地範圍攻擊（以自身為中心的圓）。  
    升級可選擇擊退效果或瞄準直線攻擊。
    """

    FORT = auto()
    """
    砲台，沿直線發射炮彈刺客。（穿透敵人）。  
    升級可選擇提高傷害並不穿透(碰到敵人即爆炸)或制空能力。
    """

    SHY_GUY = auto()
    """
    嘿呵：分散投擲多把飛刀、可以瞄準飛行單位。  
    升級可選擇增加攻速、範圍、傷害、飛刀數量或改為投擲迴旋鏢。
    """


class EnemyType(IntEnum):
    """敵人種類。"""
    BASIC = auto()


class SpellType(IntEnum):
    """技能類別。"""

    POISON = auto()
    """毒藥，對範圍內的敵人造成持續傷害。"""
    
    DOUBLE_INCOME = auto()
    """一段時間內收到的金錢變兩倍。"""
    
    TELEPORT = auto()
    """傳送我方地圖中一個區域的所有敵人到對手的場地內，重新從起點開始走。"""


class StatusCode(IntEnum):
    """呼叫API得到的回覆狀態。"""

    OK = 200
    """成功。"""

    ILLFORMED_COMMAND = 400
    """呼叫API的參數陣列不符格式。"""

    AUTH_FAIL = 401
    """我沒有看到哪裡會噴這個錯(?)"""

    ILLEGAL_ARGUMENT = 402
    """回傳值類型不符API規定。"""

    COMMAND_ERR = 403
    """也沒有看到哪裡會噴這個錯(?)"""

    NOT_FOUND = 404
    """CommandType不存在。"""

    TOO_FREQUENT = 405
    """最近兩次的API請求相隔時間過短。"""

    INTERNAL_ERR = 500
    """Godot server端出現問題（對不起！！！）。"""

    CLIENT_ERR = 501
    """Python client端出現問題。"""


class TypeCode(IntEnum):
    """基本型別代號。"""

    NULL_TYPE = 0
    """空值。"""

    BOOL_TYPE = 1
    """布林。"""

    INT_TYPE = 2
    """整數。"""

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
    """塔。"""

    def __init__(self, _type: TowerType, position: Vector2, level: int, aim: bool = True, 
                 anti_air: bool = False, bullet_number: int = 1, reload: int = 60, 
                 range: int = 100, damage: int = 10) -> None:
        self.type = _type
        """塔的型別，見class TowerType"""

        self.position = position
        """塔的座標，地圖左上角為(0, 0)。"""
        
        self.level = level
        """塔的等級。"""

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

        self.bullet_effect = 'none'
        """
        特殊效果。
        - none: 無
        - fire: 燃燒的持續傷害
        - freeze: 緩速
        - deep_freeze: 強化緩速
        - knockback: 擊退部分敵人
        - far_knockback: 擊退所有敵人
        """

class Enemy:
    """敵人(士兵)。"""

    def __init__(self, _type: EnemyType, position: Vector2, health: int, max_hp: int = None,
                 flying: bool = False, damage: int = None, armor: int = None, 
                 shield: int = None, knockback_resist: bool = False, kill_reward: int = None,
                 income_impact: int = None, cool_down: int = None) -> None:
        self.type = _type
        """敵人型別，見class EnemyType"""

        self.position = position
        """敵人座標。"""

        self.health = health
        """現行血量。"""

        self.max_hp = max_hp
        """最大血量。"""

        self.flying = flying
        """是不是空中單位。"""

        self.damage = damage
        """對塔能造成的傷害。"""

        self.armor = armor
        """
        護甲，
        若self.shield為0，則受到的傷害為塔的攻擊之max(0.2 (20-a)/20)倍。
        """

        self.shield = shield
        """
        護盾，
        若self.shield不為0，則受到的傷害為塔的攻擊與self.shield中較小者。
        """

        self.knockback_resist = knockback_resist
        """擊退抵抗，若為true則不會被擊退。"""

        self.kill_reward = kill_reward
        """擊殺該敵人會獲得的獎勵。"""

        self.income_impact = income_impact
        """派兵到對手場地後對 income 的影響，可正可負。"""

        self.cool_down = cool_down
        """派兵時間間隔。"""
