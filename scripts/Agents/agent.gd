class_name Agent
extends Node

enum TowerType { BASIC }
enum SkillType { SLOW_DOWN, DAMAGE }
@onready var game = self.get_parent()


func build(position: Vector2i, _type: TowerType) -> bool:
	if not game.can_build_tower(position):
		print("[Agent] Cannot Build Tower at ", position)
		return false
	print("[Agent] Can Build Tower at ", position)
	return true


func sell(_position: Vector2i) -> bool:
	# TODO
	return true


func upgrade(_position: Vector2i) -> bool:
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
