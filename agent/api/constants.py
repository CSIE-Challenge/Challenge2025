from enum import IntEnum


class CommandType(IntEnum):
    """每種 API 對應的編號，用於報錯訊息。"""

    GET_ALL_TERRAIN = 1
    GET_SCORES = 2
    GET_CURRENT_WAVE = 3
    GET_REMAIN_TIME = 4
    GET_TIME_UNTIL_NEXT_WAVE = 5
    GET_MONEY = 6
    GET_INCOME = 7
    GET_GAME_STATUS = 8
    GET_TERRAIN = 9
    GET_SYSTEM_PATH = 10
    GET_OPPONENT_PATH = 11
    PLACE_TOWER = 101
    GET_ALL_TOWERS = 102
    GET_TOWER = 103
    SELL_TOWER = 104
    SET_STRATEGY = 105
    SPAWN_UNIT = 201
    GET_UNIT_COOLDOWN = 202
    GET_ALL_ENEMIES = 203
    CAST_SPELL = 301
    GET_SPELL_COOLDOWN = 302
    SEND_CHAT = 401
    GET_CHAT_HISTORY = 402
    SET_CHAT_NAME_COLOR = 403
    PIXELCAT = 501
    GET_DEVS = 502
    SET_NAME = 503


class GameStatus(IntEnum):
    """遊戲運行狀態，用於查詢目前遊戲是否運行中。"""

    PREPARING = 0
    """遊戲尚未開始，正在準備中。"""

    RUNNING = 1
    """遊戲已經開始且正在進行中。"""

    PAUSED = 2
    """遊戲已經開始，但暫時被暫停中。"""


class TerrainType(IntEnum):
    """代表地圖上某一格的地形，用於查詢地圖上指定位置的地形。"""

    OUT_OF_BOUNDS = 0
    """超出邊界的區域。"""

    EMPTY = 1
    """空地，可放置塔。"""

    ROAD = 2
    """道路，是敵人行進的路徑，不可以放置塔。"""

    OBSTACLE = 3
    """障礙物，不可行走也不能放塔。"""


class TowerType(IntEnum):
    """防禦塔的種類，用於獲取防禦塔資訊或指定要放置的防禦塔種類。"""

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

    DONKEY_KONG = 3
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
    """攻擊單位的種類，用於獲取攻擊單位資訊或指定派出的攻擊單位種類。"""

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
    """技能的種類，用於查詢技能冷卻時間或指定施放的技能種類。"""

    POISON = 0
    """毒藥，對範圍內的敵人造成持續傷害。"""

    DOUBLE_INCOME = 1
    """一段時間內收到的金錢變兩倍。"""

    TELEPORT = 2
    """傳送我方地圖中一個區域的所有敵人到對手的場地內，重新從起點開始走。"""


class TargetStrategy(IntEnum):
    """防禦塔的瞄準策略，用於指定防禦塔如何瞄準攻擊單位。"""

    FIRST = 0
    """瞄準範圍內進度最快的敵人"""

    LAST = 1
    """瞄準範圍內進度最慢的敵人"""

    CLOSE = 2
    """瞄準距離自己最近的敵人"""


class ChatSource(IntEnum):
    """聊天室內的發言者，用於調閱聊天室訊息歷史。"""

    SYSTEM = 0
    """系統訊息。"""

    PLAYER_SELF = 1
    """己方的發言。"""

    PLAYER_OTHER = 2
    """對方的發言"""


class StatusCode(IntEnum):
    """呼叫 API 得到的回覆狀態，用於確認指令執行結果與錯誤處理。"""

    OK = 200
    """成功。"""

    ILLFORMED_COMMAND = 400
    """
    呼叫 API 的參數陣列不符格式。  
    ex: 參數數量錯誤。
    """

    AUTH_FAIL = 401
    """認證失敗。"""

    ILLEGAL_ARGUMENT = 402
    """API 傳入參數型別錯誤。"""

    COMMAND_ERR = 403
    """指令施放失敗。"""

    NOT_FOUND = 404
    """CommandType 不存在。"""

    TOO_FREQUENT = 405
    """最近兩次的 API 請求相隔時間過短。"""

    NOT_STARTED = 406
    """遊戲尚未開始。"""

    PAUSED = 407
    """遊戲暫停中。"""

    INTERNAL_ERR = 500
    """Godot server 端出現問題（請向開發組反映，對不起！！！）。"""

    CLIENT_ERR = 501
    """Python client 端出現問題（請向開發組反映，對不起！！！）。"""
