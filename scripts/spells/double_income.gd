class_name DoubleIncomeSpell
extends Node

static var metadata: Dictionary = {
	"name": "DoubleIncome",
	"scene_path": "res://scenes/spells/double_income.tscn",
	"description": "I am rich",
	"stats":
	{
		"duration": 10,
		"cooldown": 60,
		"target": false,
	}
}

var game: Game
var manager
var is_active: bool = false
var is_on_cooldown: bool = false
@onready var duration_timer: Timer = $DurationTimer
@onready var cooldown_timer: Timer = $CooldownTimer


func _ready() -> void:
	if get_parent().name == "SpellManager":
		manager = get_parent()
		game = manager.get_parent() as Game
		duration_timer.timeout.connect(_on_duration_ended)
		cooldown_timer.timeout.connect(_on_cooldown_ended)


func cast_spell() -> bool:
	if is_on_cooldown or is_active or not game:
		return false
	is_on_cooldown = true
	activate_effect()
	return true


func activate_effect():
	is_active = true
	var stats = metadata.stats

	game.income_rate = 2

	# Start timers
	duration_timer.wait_time = stats.duration
	cooldown_timer.wait_time = stats.cooldown
	duration_timer.start()
	cooldown_timer.start()


func _on_duration_ended():
	game.income_rate = 1
	is_active = false


func _on_cooldown_ended():
	is_on_cooldown = false
