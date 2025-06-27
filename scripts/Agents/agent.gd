class_name Agent
extends Node

enum TowerType { BASIC }
enum SkillType { SLOW_DOWN, DAMAGE }


func build(_position: Array[int], _type: TowerType) -> bool:
	# TODO
	return true


func sell(_position: Array[int]) -> bool:
	# TODO
	return true


func upgrade(_position: Array[int]) -> bool:
	# TODO
	return true


func use_skill(_position: Vector2, _type: SkillType) -> bool:
	# TODO
	return true


func get_map() -> Array:
	# TODO
	return []


func get_state():
	# TODO
	pass


func get_opponent_state():
	# TODO
	pass
