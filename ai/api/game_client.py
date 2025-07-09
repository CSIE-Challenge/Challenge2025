from .defs import *
from .game_client_base import GameClientBase, game_command

from typing import List

# the decorated member functions are dummy functions that never gets called
# an NotImplementedError is raised because returning nothing violates return type checking

class GameClient(GameClientBase):

    @game_command(CommandType.GET_ALL_TERRAIN, [bool], list[list[TerrainType]])
    def get_all_terrain(self, owned: bool) -> list[list[TerrainType]]:
        """
        # Get All Terrain
        取得地圖上所有地形的資訊。

        ## Parameters
        - `owned` (bool): 是否為玩家擁有的地圖。如果為 `True`，則查詢玩家擁有的地圖，如果為 `False`，則查詢對手擁有的地圖。

        ## Returns
        這個函數返回一個二維陣列，表示地圖上所有地形的資訊。每個元素都是一個 `TerrainType` 枚舉類型，表示該位置的地形類型。
        
        ## TerrainType
        
        - OUT_OF_BOUNDS: 表示超出邊界的區域。
        - EMPTY: 表示空地。可以放置塔。
        - ROAD: 表示道路。是敵人行進的路徑。不可以放置塔。
        - OBSTACLE: 表示障礙物。不可以放置塔。

        ## Example
        ```python
        terrain_map = api.get_all_terrain(owned=True)  # 獲取整個地圖的地形資訊
        for row in terrain_map:
            print(row)
        ```
        """
        raise NotImplementedError
    
    @game_command(CommandType.GET_TERRAIN, [bool, Vector2], TerrainType)
    def get_terrain(self, owned: bool, pos: Vector2) -> TerrainType:
        """
        # Get Terrain
        取得指定位置的地形資訊。

        ## Parameters
        - `owned` (bool): 是否為玩家擁有的地圖。如果為 `True`，則查詢玩家擁有的地圖，如果為 `False`，則查詢對手擁有的地圖。
        - `pos` (Vector2): 要查詢的地形位置。

        ## Returns
        這個函數返回一個 `TerrainType` 枚舉類型，表示指定位置的地形類型。

        ## TerrainType
        - OUT_OF_BOUNDS: 表示超出邊界的區域。
        - EMPTY: 表示空地。可以放置塔。
        - ROAD: 表示道路。是敵人行進的路徑。不可以放置塔。
        - OBSTACLE: 表示障礙物。不可以放置塔。

        ## Example
        ```python
        terrain = api.get_terrain(True, Vector2(5, 10))  # 獲取玩家擁有地圖上 (5, 10) 的地形
        opponent_terrain = api.get_terrain(False, Vector2(3, 7))  # 獲取對手擁有地圖上 (3, 7) 的地形
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

        ## Returns
        這個函數返回一個整數，表示指定玩家的分數。

        ## Example
        ```python
        score = api.get_scores(True)  # 獲取玩家的分數
        opponent_score = api.get_scores(False)  # 獲取對手的分數
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.SEND_CHAT, [str], bool)
    def send_chat(self, msg: str) -> bool:
        raise NotImplementedError
    
    @game_command(CommandType.GET_CHAT_HISTORY, [int], list[tuple[int, str]])
    def get_chat_history(self, num: int) -> list[tuple[int, str]]:
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
        money = api.get_money(owned=True)  # 獲取玩家的金錢數量
        opponent_money = api.get_money(owned=False)  # 獲取對手的金錢數量
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_INCOME, [bool], int)
    def get_income(self, owned: bool) -> int:
        """
        # Get Income
        取得玩家或對手的收入。

        ## Parameters
        - `owned` (bool): 是否為玩家自己的收入。如果為 `True`，則差尋玩家的收入，如果為 `False`，則查詢對手的收入。

        ## Returns
        這個函數返回一個整數，表示指定玩家的收入。

        ## Example
        ```python
        income = api.get_income(owned=True) # 獲取玩家的收入
        opponent_income = api.get_income(owned=False)  # 獲取對手的收入
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
        current_wave = api.get_current_wave()  # 獲取當前波數
        print(f"Current wave: {current_wave}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_REMAIN_TIME, [], float)
    def get_remain_time(self) -> float:
        """
        # Get Remain Time
        取得當前波次剩餘的時間。

        ## Parameters
        無參數
        
        ## Returns
        這個函數返回一個浮點數，表示剩餘的時間，單位為秒。

        ## Example
        ```python
        remain_time = api.get_remain_time()  # 獲取當前波次剩餘的時間
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
        time_until_next_wave = api.get_time_until_next_wave()  # 獲取距離下一波開始的時間
        print(f"Time until next wave: {time_until_next_wave} seconds")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.PLACE_TOWER, [TowerType, Vector2], None)
    def place_tower(self, type: TowerType, coord: Vector2) -> None:
        """
        # Place Tower
        在指定位置放置一個塔。

        ## Parameters
        - `type` (TowerType): 要放置的塔的類型。
        - `coord` (Vector2): 要放置塔的位置。

        ## Returns
        這個函數沒有返回值。如果放置成功，則塔會被放置在指定位置。

        ## TowerType
        - TODO
        
        ## Example
        ```python
        api.place_tower(TowerType.BASIC, Vector2(5, 10))  # 在 (5, 10) 的位置放置一個基本塔
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ALL_TOWERS, [bool], list)
    def get_all_towers(self, owned: bool) -> List[TowerType]:
        """
        # Get All Towers
        取得所有塔的資訊。

        ## Parameters
        - `owned` (bool): 是否查詢玩家自己的塔。

        ## Returns
        這個函數返回一個 `Tower` 物件的列表。

        ## Example
        ```python
        towers = api.get_all_towers(owned=True)  # 獲取玩家自己的所有塔
        for tower in towers:
            print(tower)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_TOWER, [Vector2], TowerType)
    def get_tower(self, coord: Vector2) -> TowerType:
        """
        # Get Tower
        取得指定位置的塔的資訊。

        ## Parameters
        - `coord` (Vector2): 要查詢的位置。

        ## Returns
        這個函數返回一個 `Tower` 物件。

        ## Example
        ```python
        tower = api.get_tower(Vector2(5, 10))  # 獲取 (5, 10) 位置的塔資訊
        print(tower)
        """
        raise NotImplementedError

    @game_command(CommandType.SPAWN_ENEMY, [EnemyType], None)
    def spawn_enemy(self, type: EnemyType) -> None:
        """
        # Spawn Enemy
        派出一個指定類型的敵人。

        ## Parameters
        - `type` (EnemyType): 要派出的敵人的類型。

        ## Returns
        這個函數沒有返回值。如果派出成功，則敵人會被加入到遊戲中。

        ## EnemyType
        - TODO
        
        ## Example
        ```python
        api.spawn_enemy(EnemyType.BASIC)  # 派出一個基本敵人
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ENEMY_COOLDOWN, [bool, EnemyType], int)
    def get_enemy_cooldown(self, owned: bool, type: EnemyType) -> int:
        """
        # Get Enemy Cooldown
        取得指定類型敵人的冷卻時間。

        ## Parameters
        - `owned` (bool): 是否查詢玩家自己的冷卻時間。
        - `type` (EnemyType): 要查詢的敵人類型。

        ## Returns
        這個函數返回一個整數，表示冷卻時間。

        ## EnemyType
        - TODO

        ## Example
        ```python
        cooldown = api.get_enemy_cooldown(True, EnemyType.BASIC)  # 獲取玩家自己的基本敵人的冷卻時間
        print(f"Cooldown for my BASIC enemy: {cooldown} seconds")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ENEMY_INFO, [EnemyType], EnemyType)
    def get_enemy_info(self, type: EnemyType) -> EnemyType:
        """
        # Get Enemy Info
        取得指定類型敵人的資訊。

        ## Parameters
        - `type` (EnemyType): 要查詢的敵人類型。

        ## Returns
        這個函數返回一個 `Enemy` 物件。

        ## EnemyType
        - TODO

        ## Example
        ```python
        enemy_info = api.get_enemy_info(EnemyType.BASIC)  # 獲取基本敵人的資訊
        print(enemy_info)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_AVAILABLE_ENEMIES, [], list)
    def get_available_enemies(self) -> List[EnemyType]:
        """
        # Get Available Enemies
        取得所有可用的敵人資訊。

        ## Returns
        這個函數返回一個 `Enemy` 物件的列表。

        ## Example
        ```python
        available_enemies = api.get_available_enemies()  # 獲取所有可用的敵人資訊
        for enemy in available_enemies:
            print(enemy)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_CLOSEST_ENEMIES, [Vector2, int], list)
    def get_closest_enemies(self, position: Vector2, count: int) -> List[EnemyType]:
        """
        # Get Closest Enemies
        取得離指定位置最近的敵人。

        ## Parameters
        - `position` (Vector2): 要查詢的位置。
        - `count` (int): 要查詢的敵人數量。

        ## Returns
        這個函數返回一個 `Enemy` 物件的列表。

        ## Example
        ```python
        closest_enemies = api.get_closest_enemies(Vector2(5, 10), 3)  # 獲取離 (5, 10) 最近的 3 個敵人
        for enemy in closest_enemies:
            print(enemy)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_ENEMIES_IN_RANGE, [Vector2, float], list)
    def get_enemies_in_range(self, center: Vector2, radius: float) -> List[EnemyType]:
        """
        # Get Enemies in Range
        取得在指定範圍內的敵人。

        ## Parameters
        - `center` (Vector2): 範圍的中心點。
        - `radius` (float): 範圍的半徑。

        ## Returns
        這個函數返回一個 `Enemy` 物件的列表。

        ## Example
        ```python
        enemies_in_range = api.get_enemies_in_range(Vector2(5, 10), 5.0)  # 獲取在 (5, 10) 中心點，半徑為 5 的範圍內的敵人
        for enemy in enemies_in_range:
            print(enemy)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.CAST_SPELL, [SpellType, Vector2], None)
    def cast_spell(self, type: SpellType, position: Vector2) -> None:
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
        api.cast_spell(SpellType.POISON, Vector2(5, 10))  # 在 (5, 10) 的位置施放毒藥法術
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
        cooldown = api.get_spell_cooldown(True, SpellType.POISON)  # 獲取玩家自己的毒藥法術的冷卻時間
        print(f"Cooldown for my POISON spell: {cooldown} seconds")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_SPELL_COST, [SpellType], float)
    def get_spell_cost(self, type: SpellType) -> float:
        """
        # Get Spell Cost
        取得法術的消耗。

        ## Parameters
        - `type` (SpellType): 要查詢的法術類型。

        ## Returns
        這個函數返回一個浮點數，表示法術的消耗。

        ## SpellType
        - POISON: 毒藥法術，對範圍內的敵人造成持續傷害。
        - DOUBLE_INCOME: 雙倍收入法術，在一段時間內使玩家的所有收入來源變為兩倍。
        - TELEPORT: 傳送法術，將敵人傳送到對手的路線起點。

        ## Example
        ```python
        cost = api.get_spell_cost(SpellType.POISON)  # 獲取毒藥法術的消耗
        print(f"Cost for POISON spell: {cost} money")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_EFFECTIVE_SPELLS, [bool], list)
    def get_effective_spells(self, owned: bool) -> List[SpellType]:
        """
        # Get Effective Spells
        取得當前生效的法術。

        ## Parameters
        - `owned` (bool): 是否查詢玩家自己的法術。

        ## Returns
        這個函數返回一個 `Spell` 物件的列表。

        ## Example
        ```python
        effective_spells = api.get_effective_spells(True)  # 獲取玩家自己的生效法術
        for spell in effective_spells:
            print(spell)
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.SEND_CHAT, [str], bool)
    def send_chat(self, msg: str) -> bool:
        """
        # Send Chat
        發送一條聊天訊息。

        ## Parameters
        - `msg` (str): 要發送的訊息。

        ## Returns
        這個函數返回一個布林值，表示訊息是否發送成功。

        ## Example
        ```python
        success = api.send_chat("Hello, my friend!")  # 發送聊天訊息
        if success:
            print("Message sent successfully!")
        else:
            print("Failed to send message.")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.GET_CHAT_HISTORY, [int], list)
    def get_chat_history(self, num: int = 15) -> list[tuple[int, str]]:
        """
        # Get Chat History
        取得聊天歷史紀錄。

        ## Parameters
        - `num` (int): 要取得的訊息數量，預設為 15。

        ## Returns
        這個函數返回一個元組列表，每個元組包含傳訊人 ID 和訊息。

        ## Example
        ```python
        chat_history = api.get_chat_history(10)  # 獲取最近的 10 條聊天訊息
        for id, message in chat_history:
            print(f"[{id}] {message}")
        ```
        """
        raise NotImplementedError

    @game_command(CommandType.PIXELCAT, [], str)
    def pixelcat(self) -> str:
        """
        # Pixel Cat
        取得一隻像素貓的圖像。

        ## Parameters
        無參數

        ## Returns
        這個函數返回一個字串，表示像素貓的 ASCII 藝術。

        ## Example
        ```python
        pixel_cat = api.pixelcat()  # 獲取像素貓的 ASCII 藝術
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
        devs = api.get_devs()  # 獲取開發者名單
        for dev in devs:
            print(dev)
        ```
        """
        raise NotImplementedError
    
    @game_command(CommandType.GET_ALL_TOWERS, [bool], TowerType)
    def get_all_towers(self, owned: bool) -> list[TowerType]:
        raise NotImplementedError

    @game_command(CommandType.GET_TOWER, [Vector2], TowerType)
    def get_tower(self, coord: Vector2) -> TowerType:
        raise NotImplementedError
