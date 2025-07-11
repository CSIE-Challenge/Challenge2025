class_name TeleportSpell
extends Node
static var metadata: Dictionary = {
	"name": "Teleport",
	"scene_path": "res://scenes/spells/teleport.tscn",
	"description": "I need some ender pearls",
	"stats":
	{
		"duration": 1,
		"cooldown": 60,
		"cost": 0,
		"target": true,
		"radius": 30.0,
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
	var effect = preload("res://scenes/spells/teleport_effect.tscn").instantiate()

	add_child(effect)
	effect.global_position = global_pos

	# Start timers
	cooldown_timer.wait_time = stats.cooldown
	is_on_cooldown = true
	cooldown_timer.start()


func _on_cooldown_ended():
	is_on_cooldown = false
