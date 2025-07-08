class_name PoisonSpell
extends Node
static var metadata: Dictionary = {
	"name": "Poison",
	"scene_path": "res://scenes/spells/poison.tscn",
	"description": "Don't be toxic",
	"stats":
	{
		"duration": 20,
		"cooldown": 40,
		"cost": 50,
		"target": true,
		"radius": 50.0,
		"trigger_interval": 2,
		"trigger_damage": 2,
	}
}
var game: Game
var manager
var is_on_cooldown: bool = false
@onready var range_indicator: RangeIndicator = $Range
@onready var cooldown_timer: Timer = $CooldownTimer


func _ready() -> void:
	if get_parent().name == "SpellManager":
		manager = get_parent()
		game = manager.get_parent() as Game
		cooldown_timer.timeout.connect(_on_cooldown_ended)


func cast_spell(global_pos: Vector2i) -> bool:
	if is_on_cooldown or not game:
		print("Spell is on cooldown! Wait ", cooldown_timer.get_time_left(), " seconds")
		return false
	if not game.spend(metadata.stats.cost):
		print("Not enough money")
		return false
	activate_effect(global_pos)
	return true


func activate_effect(global_pos: Vector2):
	var stats = metadata.stats
	var effect = preload("res://scenes/spells/poison_effect.tscn").instantiate()

	add_child(effect)
	effect.global_position = global_pos

	# Start timers
	cooldown_timer.wait_time = stats.cooldown
	cooldown_timer.start()


func _on_cooldown_ended():
	is_on_cooldown = false
