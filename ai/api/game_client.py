from .defs import *
from .game_client_base import GameClientBase, game_command


# the decorated member functions are dummy functions that never gets called
# an NotImplementedError is raised because returning nothing violates return type checking

class GameClient(GameClientBase):

    @game_command(CommandType.GET_ALL_TERRAIN, [], TerrainType)
    def get_all_terrain(self) -> list[list[TerrainType]]:
        """
        # Get All Terrain
        取得地圖上所有地形的資訊。

        ## Parameters
        無參數。

        ## Returns
        這個函數返回一個二維陣列，表示地圖上所有地形的資訊。每個元素都是一個 `TerrainType` 枚舉類型，表示該位置的地形類型。
        
        ## TerrainType
        
        - OUT_OF_BOUNDS: 表示超出邊界的區域。
        - EMPTY: 表示空地。可以放置塔。
        - ROAD: 表示道路。是敵人行進的路徑。不可以放置塔。
        - OBSTACLE: 表示障礙物。不可以放置塔。

        ## Example
        ```python
        terrain_map = api.get_all_terrain()  # 獲取整個地圖的地形資訊
        for row in terrain_map:
            print(row)  # 每一行都是一個地形類型的列表
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
