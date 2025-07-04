class_name Agent
extends Node

enum AgentType { HUMAN, AI, NIL }
enum TowerType { BASIC }
enum SkillType { SLOW_DOWN, DAMAGE }
enum StatusCode {
	OK = 200,
	ILLFORMED_COMMAND = 400,
	AUTH_FAIL = 401,
	ILLEGAL_ARGUMENT = 402,
	COMMAND_ERR = 403,
	NOT_FOUND = 404,
	INTERNAL_ERR = 500
}
var type: AgentType = AgentType.NIL

@onready var game = self.get_parent()


func get_all_terrain() -> Array:
	return [StatusCode.OK]


func get_scores(_owned: bool) -> Array:
	return [StatusCode.OK]


func get_current_wave() -> Array:
	return [StatusCode.OK]


func get_remain_time() -> Array:
	return [StatusCode.OK]


func get_time_until_next_wave() -> Array:
	return [StatusCode.OK]


func get_money(_owned: bool) -> Array:
	return [StatusCode.OK]


func get_income(_owned: bool) -> Array:
	return [StatusCode.OK]
