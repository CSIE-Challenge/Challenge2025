extends Node

enum CommandType { BUILD, SELL, UPGRADE, GET_MAP, GET_PLAYER_STATE, GET_OPPONENT_STATE }


class Command:
	var type: CommandType
