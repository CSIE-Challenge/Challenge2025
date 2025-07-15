from .constants import (
    CommandType,
    GameStatus,
    TerrainType,
    TowerType,
    EnemyType,
    ChatSource,
    SpellType,
    TargetStrategy,
)
from .structures import (
    Vector2,
    Tower,
    Enemy,
)
from .game_client_base import GameClientBase, game_command

# the decorated member functions are dummy functions that never gets called
# an NotImplementedError is raised because returning nothing violates return type checking


class GameClient(GameClientBase):
    @game_command(CommandType.GET_GAME_STATUS, [], GameStatus)
    def get_game_status(self) -> GameStatus:
        """
        # Get Game Status
        取得現在的遊戲狀態。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個 `GameStatus` 枚舉類型，表示目前的遊戲狀態。

        ## Example
        ```python
        status = agent.get_game_status()
        while status != GameStatus.RUNNING:
            time.sleep(1)
            status = agent.get_game_status()
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ALL_TERRAIN, [], list[list[TerrainType]])
    def get_all_terrain(self) -> list[list[TerrainType]]:
        """
        # Get All Terrain
        取得地圖上所有地形的資訊。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個二維陣列，表示地圖上所有地形的資訊。每個元素都是一個 `TerrainType` 枚舉類型，表示該位置的地形類型。

        ## Example
        ```python
        terrain_map = agent.get_all_terrain()  # 獲取整個地圖的地形資訊
        for row in terrain_map:
            print(row)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_TERRAIN, [Vector2], TerrainType)
    def get_terrain(self, pos: Vector2) -> TerrainType:
        """
        # Get Terrain
        取得指定位置的地形資訊。

        ## Parameters
        - `pos` (Vector2): 要查詢的地形位置。

        ## Returns
        這個函數返回一個 `TerrainType` 枚舉類型，表示指定位置的地形類型。

        ## Example
        ```python
        terrain = agent.get_terrain(Vector2(5, 10))  # 獲取玩家擁有地圖上 (5, 10) 的地形
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_SCORES, [bool], int)
    def get_scores(self, owned: bool) -> int:
        """
        # Get Scores
        取得玩家或對手的分數。

        ## Parameters
        - `owned` (bool): 是否為玩家擁有的分數。如果為 `True`，則查詢玩家的分數，如果為 `False`，則查詢對手的分數。
          如果遊戲的記分板被凍結，獲取對手的分數將為記分板凍結瞬間的分數而非實際分數。

        ## Returns
        這個函數返回一個整數，表示指定玩家的分數。

        ## Example
        ```python
        score = agent.get_scores(True)  # 獲取玩家的分數
        opponent_score = agent.get_scores(False)  # 獲取對手的分數
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_MONEY, [bool], int)
    def get_money(self, owned: bool) -> int:
        """
        # Get Money
        取得玩家或對手的金錢數量。

        ## Parameters
        - `owned` (bool): 是否為玩家擁有的金錢。如果為 `True`，則查詢玩家的金錢，如果為 `False`，則查詢對手的金錢。

        ## Returns
        這個函數返回一個整數，表示指定玩家的金錢數量。

        ## Example
        ```python
        money = agent.get_money(True)  # 獲取玩家的金錢數量
        opponent_money = agent.get_money(False)  # 獲取對手的金錢數量
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_INCOME, [bool], int)
    def get_income(self, owned: bool) -> int:
        """
        # Get Income
        取得玩家或對手的收入。

        ## Parameters
        - `owned` (bool): 是否為玩家自己的收入。如果為 `True`，則查詢玩家的收入，如果為 `False`，則查詢對手的收入。

        ## Returns
        這個函數返回一個整數，表示指定玩家的收入。

        ## Example
        ```python
        income = agent.get_income(True) # 獲取玩家的收入
        opponent_income = agent.get_income(False)  # 獲取對手的收入
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_CURRENT_WAVE, [], int)
    def get_current_wave(self) -> int:
        """
        # Get Current Wave
        取得當前的波數。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個整數，表示當前的波數。

        ## Example
        ```python
        current_wave = agent.get_current_wave()  # 獲取當前波數
        print(f"Current wave: {current_wave}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_REMAIN_TIME, [], float)
    def get_remain_time(self) -> float:
        """
        # Get Remain Time
        取得遊戲剩餘的時間。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個浮點數，表示遊戲剩餘的時間，單位為秒。

        ## Example
        ```python
        remain_time = agent.get_remain_time()  # 獲取遊戲剩餘的時間
        print(f"Remaining time: {remain_time} seconds")
        """
        raise NotImplementedError

    @game_command(CommandType.GET_TIME_UNTIL_NEXT_WAVE, [], float)
    def get_time_until_next_wave(self) -> float:
        """
        # Get Time Until Next Wave
        取得距離下一波開始的時間。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個浮點數，表示距離下一波的時間，單位為秒。

        ## Example
        ```python
        time_until_next_wave = agent.get_time_until_next_wave()  # 獲取距離下一波開始的時間
        print(f"Time until next wave: {time_until_next_wave} seconds")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_SYSTEM_PATH, [bool], list[Vector2])
    def get_system_path(self, fly: bool) -> list[Vector2]:
        """
        # Get System Path
        取得系統派兵的路徑。

        ## Parameters
        - `fly` (bool): 是否為飛行兵的路徑。

        ## Returns
        這個函式返回一個座標陣列，表示系統派兵從起點到終點經過的格點。

        ## Example
        ```python
        system_path = agent.get_system_path(False) # 獲取系統派地面兵路徑
        for cell in system_path:
            print(f"x:{cell.x}, y:{cell.y}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_OPPONENT_PATH, [bool], list[Vector2])
    def get_opponent_path(self, fly: bool) -> list[Vector2]:
        """
        # Get Opponent Path
        取得對手派兵的路徑。

        ## Parameters
        - `fly` (bool): 是否為飛行兵的路徑。

        ## Returns
        這個函式返回一個座標陣列，表示對手派兵從起點到終點經過的格點。

        ## Example
        ```python
        opp_path = agent.get_opponent_path(True) # 獲取對手派飛行兵路徑
        for cell in opp_path:
            print(f"x:{cell.x}, y:{cell.y}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.PLACE_TOWER, [TowerType, str, Vector2], None)
    def place_tower(self, type: TowerType, level: str, coord: Vector2) -> None:
        """
        # Place Tower
        在指定位置放置或升級一個塔。

        ## Parameters
        - `type` (TowerType): 要放置的塔的類型。
        - `level` (str): 要放置的塔的等級，可為"1", "2a", "2b", "3a", "3b"。數字表示等級，a和b是不同的升級分支，升級時不可以切換分支。
        - `coord` (Vector2): 要放置塔的位置。

        ## Returns
        這個函數沒有返回值。如果放置成功，則塔會被放置在指定位置。

        ## TowerType
        - 有FIRE_MARIO, ICE_LUIGI, DONKEY_KONG, FORT, SHY_GUY五種。

        ## Example
        ```python
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(5, 10))  # 在 (5, 10) 的位置放置一個馬力歐塔
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ALL_TOWERS, [bool], list[Tower])
    def get_all_towers(self, owned: bool) -> list[Tower]:
        """
        # Get All Towers
        取得所有塔的資訊。

        ## Parameters
        - `owned` (bool): 查詢自己 (True) 或對手 (False) 的塔。

        ## Returns
        這個函數返回一個 `Tower` 物件的列表。

        ## Example
        ```python
        towers = agent.get_all_towers(True)  # 獲取玩家自己的所有塔
        for tower in towers:
            print(tower)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_TOWER, [bool, Vector2], Tower)
    def get_tower(self, owned: bool, coord: Vector2) -> Tower:
        """
        # Get Tower
        取得自己的地圖中指定位置上塔的資訊。

        ## Parameters
        - `owned` (bool): 查詢自己 (True) 或對手 (False) 的塔。
        - `coord` (Vector2): 要查詢的位置。

        ## Returns
        這個函數返回一個 `Tower` 物件。

        ## Example
        ```python
        tower = agent.get_tower(Vector2(5, 10))  # 獲取 (5, 10) 位置的塔資訊
        print(tower)
        """
        raise NotImplementedError

    @game_command(CommandType.SELL_TOWER, [Vector2], None)
    def sell_tower(self, coord: Vector2) -> None:
        """
        # Sell Tower
        賣掉地圖中指定位置上的一座防禦塔。

        ## Parameters
        - `coord` (Vector2): 要賣掉的防禦塔的位置。

        ## Returns
        這個函數沒有返回值。如果成功的話，指定位置上的防禦塔會被賣掉。

        ## Example
        agent.sell_tower(Vector2(5, 10))  # 賣掉 (5, 10) 的位置上的防禦塔
        """
        raise NotImplementedError

    @game_command(CommandType.SET_STRATEGY, [Vector2, TargetStrategy], None)
    def set_strategy(self, coord: Vector2, strategy: TargetStrategy) -> None:
        """
        # Set Strategy
        指定一座防禦塔的瞄準策略。

        ## Parameters
        - `coord` (Vector2): 欲變更瞄準策略的防禦塔位置。
        - `strategy` (TargetStrategy): 該防禦塔新的的瞄準策略，有FIRST，LAST和CLOSE。

        ## Returns
        這個函數沒有返回值。如果成功的話，防禦塔的瞄準策略會被變更。

        ## Example
        agent.set_strategy(Vector2(5, 10), CLOSE)  # 將 (5, 10) 的位置上的防禦塔的瞄準策略改成瞄準最近的敵人單位。
        """
        raise NotImplementedError

    @game_command(CommandType.SPAWN_UNIT, [EnemyType], None)
    def spawn_unit(self, type: EnemyType) -> None:
        """
        # Spawn Unit
        派出一個指定類型的單位。

        ## Parameters
        - `type` (EnemyType): 要派出的單位的類型。

        ## Returns
        這個函數沒有返回值。如果派出成功，則敵人會被加入到遊戲中。

        ## Example
        ```python
        agent.spawn_enemy(EnemyType.GOOMBA)  # 派出 GOOMBA
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_UNIT_COOLDOWN, [EnemyType], float)
    def get_unit_cooldown(self, type: EnemyType) -> float:
        """
        # Get Unit Cooldown
        取得特定單位的派遣冷卻時間。

        ## Parameters
        - `type` (EnemyType): 要查詢的單位的類型。

        ## Returns
        這個函數返回一個浮點數，代表此類型的單位再過幾秒後可以再次派遣。

        ## Example
        ```python
        to_wait = agent.get_unit_cooldown(EnemyType.KOOPA)
        time.sleep(to_wait)  # 等待直到可以再次派出一隻 KOOPA
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ALL_ENEMIES, [bool], list[Enemy])
    def get_all_enemies(self, owned: bool) -> list[Enemy]:
        """
        # Get All Enemies
        取得自己地圖上所有敵人的資訊。

        ## Parameters
        - `owned` (bool): 查詢自己 (True) 或對手 (False) 的敵人。

        ## Returns
        這個函數返回一個 `Enemy` 物件的列表。

        ## Example
        ```python
        all_enemies = agent.get_all_enemies()  # 獲取自己地圖上所有敵人的資訊
        for enemy in all_enemies:
            print(enemy)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.CAST_SPELL, [SpellType, Vector2], None)
    def cast_spell(self, type: SpellType, position: Vector2 = Vector2(0, 0)) -> None:
        """
        # Cast Spell
        施放一個法術。

        ## Parameters
        - `type` (SpellType): 要施放的法術類型。
        - `position` (Vector2): 法術施放的位置。

        ## Returns
        這個函數沒有返回值。如果施放成功，則法術會被施放到指定位置。

        ## SpellType
        - POISON: 毒藥法術，對範圍內的敵人造成持續傷害。
        - DOUBLE_INCOME: 雙倍收入法術，在一段時間內使玩家的所有收入來源變為兩倍。
        - TELEPORT: 傳送法術，將敵人傳送到對手的路線起點。

        ## Example
        ```python
        agent.cast_spell(SpellType.POISON, Vector2(5, 10))  # 在 (5, 10) 的位置施放毒藥法術
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_SPELL_COOLDOWN, [bool, SpellType], float)
    def get_spell_cooldown(self, owned: bool, type: SpellType) -> float:
        """
        # Get Spell Cooldown
        取得法術的冷卻時間。

        ## Parameters
        - `owned` (bool): 是否查詢玩家自己的冷卻時間。
        - `type` (SpellType): 要查詢的法術類型。

        ## Returns
        這個函數返回一個浮點數，表示冷卻時間。

        ## SpellType
        - POISON: 毒藥法術，對範圍內的敵人造成持續傷害。
        - DOUBLE_INCOME: 雙倍收入法術，在一段時間內使玩家的所有收入來源變為兩倍。
        - TELEPORT: 傳送法術，將敵人傳送到對手的路線起點。

        ## Example
        ```python
        cooldown = agent.get_spell_cooldown(True, SpellType.POISON)  # 獲取玩家自己的毒藥法術的冷卻時間
        print(f"Cooldown for my POISON spell: {cooldown} seconds")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.SEND_CHAT, [str], None)
    def send_chat(self, msg: str) -> None:
        """
        # Send Chat
        發送一條聊天訊息。

        ## Parameters
        - `msg` (str): 要發送的訊息。

        ## Returns
        這個函數沒有返回值。如果發送成功，訊息會出現在對話框。

        ## Example
        ```python
        success = agent.send_chat("Hello, my friend!")  # 發送聊天訊息
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_CHAT_HISTORY, [int], list[tuple[ChatSource, str]])
    def get_chat_history(self, num: int = 15) -> list[tuple[ChatSource, str]]:
        """
        # Get Chat History
        取得聊天歷史紀錄。

        ## Parameters
        - `num` (int): 要取得的訊息數量，預設為 15。

        ## Returns
        這個函數返回一個元組列表，每個元組包含傳訊人 ID 和訊息。

        ## Example
        ```python
        chat_history = agent.get_chat_history(10)  # 獲取最近的 10 條聊天訊息
        for id, message in chat_history:
            print(f"[{id}] {message}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.SET_CHAT_NAME_COLOR, [str], None)
    def set_chat_name_color(self, color: str) -> None:
        """
        # Set Name
        設定對話框的玩家名字顏色

        ## Parameters
        - `color` (str): 表示顏色的十六進位制。

        ## Returns
        這個函數沒有回傳值。

        ## Example
        ```python
        agent.set_chat_name_color("ffffff") # 設定對話框的玩家名字顏色為白色
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.PIXELCAT, [], str)
    def pixelcat(self) -> str:
        """
        # Pixel Cat
        取得一隻像素貓的圖像並在聊天室發出，僅能使用一次。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個字串，表示像素貓的 ASCII 藝術。

        ## Example
        ```python
        pixel_cat = agent.pixelcat()  # 獲取像素貓的 ASCII 藝術
        print(pixel_cat)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_DEVS, [], list[str])
    def get_devs(self) -> list[str]:
        """
        # Get Devs
        取得開發者名單。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個字串列表，表示開發者的名字。

        ## Example
        ```python
        devs = agent.get_devs()  # 獲取開發者名單
        for dev in devs:
            print(dev)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.SET_NAME, [str], None)
    def set_name(self, name: str) -> None:
        """
        # Set Name
        設定玩家名稱

        ## Parameters
        - `name` (str): 玩家名稱，限制十個字元以內，一個中文字算兩個字元。

        ## Returns
        這個函數沒有回傳值。

        ## Example
        ```python
        agent.set_name("PixelCat") # 設定玩家名稱為 PixelCat
        ```
        """
        raise NotImplementedError
