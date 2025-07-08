class_name DoubleIncomeSpell
extends Node

static var metadata: Dictionary = {
	"name": "DoubleIncome",
	"scene_path": "res://scenes/spells/double_income.tscn",
	"description": "I am rich",
	"stats":
	{
		"duration": 8,
		"cooldown": 20,
		"cost": 20,
		"target": false,
	}
}

var game: Game
var manager
var duration_timer: Timer
var cooldown_timer: Timer
var is_active: bool = false
var is_on_cooldown: bool = false


func _ready() -> void:
	if get_parent().name == "SpellManager":
		manager = get_parent()
		game = manager.get_parent() as Game
		create_timers()


func create_timers():
	# Create duration timer
	duration_timer = Timer.new()
	duration_timer.one_shot = true
	duration_timer.timeout.connect(_on_duration_ended)
	add_child(duration_timer)

	# Create cooldown timer
	cooldown_timer = Timer.new()
	cooldown_timer.one_shot = true
	cooldown_timer.timeout.connect(_on_cooldown_ended)
	add_child(cooldown_timer)


func cast_spell() -> bool:
	if is_on_cooldown or is_active or not game:
		print("Spell is on cooldown! Wait ", cooldown_timer.get_time_left(), " seconds")
		return false
	if not game.spend(metadata.stats.cost):
		print("Not enough money")
		return false
	activate_effect()
	return true


func activate_effect():
	is_active = true
	var stats = metadata.stats

	if game:
		game.income_rate = 2

	# Start timers
	duration_timer.wait_time = stats.duration
	cooldown_timer.wait_time = stats.cooldown
	duration_timer.start()
	cooldown_timer.start()

	print("Double income activated for ", stats.duration, " seconds!")


func _on_duration_ended():
	if game:
		game.income_rate = 1

	is_active = false
	print("Double income effect ended!")


func _on_cooldown_ended():
	is_on_cooldown = false
	print("Double income spell ready to cast again!")
