from .defs import *
from .game_client_base import GameClientBase, game_command


# the decorated member functions are dummy functions that never gets called
# an NotImplementedError is raised because returning nothing violates return type checking

class GameClient(GameClientBase):

    @game_command(CommandType.GET_ALL_TERRAIN, [], TerrainType)
    def get_all_terrain(self) -> list[list[TerrainType]]:
        raise NotImplementedError

    @game_command(CommandType.GET_SCORES, [bool], int)
    def get_scores(self, owned: bool) -> int:
        raise NotImplementedError

    @game_command(CommandType.SEND_CHAT, [str], bool)
    def send_chat(self, msg: str) -> bool:
        raise NotImplementedError
    
    @game_command(CommandType.GET_CHAT_HISTORY, [int], list)
    def get_chat_history(self, num: int) -> list[str]:
        raise NotImplementedError

    @game_command(CommandType.GET_MONEY, [bool], int)
    def get_money(self, owned: bool) -> int:
        raise NotImplementedError

    @game_command(CommandType.GET_INCOME, [bool], int)
    def get_income(self, owned: bool) -> int:
        raise NotImplementedError
