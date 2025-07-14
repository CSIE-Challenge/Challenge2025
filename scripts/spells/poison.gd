class_name PoisonSpell
extends Node
static var metadata: Dictionary = {
	"name": "Poison",
	"scene_path": "res://scenes/spells/poison.tscn",
	"description": "Don't be toxic",
	"stats":
	{
		"duration": 5,
		"cooldown": 60,
		"target": true,
		"radius": 50,
		"trigger_interval": 0.2,
		"trigger_damage": 20,
	}
}
var game: Game
var manager
var is_on_cooldown: bool = false
var trigger_times: int = 50
var next_effect_pos: Vector2
@onready var range_indicator: RangeIndicator = $Range
@onready var cooldown_timer: Timer = $CooldownTimer
@onready var trigger_timer: Timer = $TriggerTimer


func _ready() -> void:
	if get_parent().name == "SpellManager":
		manager = get_parent()
		game = manager.get_parent() as Game
		cooldown_timer.timeout.connect(_on_cooldown_ended)
		trigger_timer.timeout.connect(_on_trigger, CONNECT_REFERENCE_COUNTED)


func cast_spell(global_pos: Vector2i) -> bool:
	if is_on_cooldown or not game:
		print("Spell is on cooldown! Wait ", cooldown_timer.get_time_left(), " seconds")
		return false
	activate_effect(global_pos)
	return true


func activate_effect(global_pos: Vector2):
	var stats = metadata.stats
	next_effect_pos = global_pos
	trigger_times = int(stats.duration / stats.trigger_interval)
	trigger_timer.wait_time = stats.trigger_interval
	trigger_timer.start()
	for i in range(trigger_times):
		trigger_timer.timeout.connect(_on_trigger, CONNECT_REFERENCE_COUNTED)

	# Start timers
	cooldown_timer.wait_time = stats.cooldown
	is_on_cooldown = true
	cooldown_timer.start()


func _on_cooldown_ended():
	is_on_cooldown = false


func _on_trigger():
	var stats = metadata.stats
	var effect = preload("res://scenes/spells/poison_effect.tscn").instantiate()

	add_child(effect)
	effect.z_index = 8
	effect.global_position = next_effect_pos

	if trigger_times > 0:
		trigger_times -= 1
	else:
		trigger_timer.stop()
