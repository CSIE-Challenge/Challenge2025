class_name TeleportSpell
extends Node
static var metadata: Dictionary = {
	"name": "Teleport",
	"scene_path": "res://scenes/spells/teleport.tscn",
	"description": "I am rich",
	"stats":
	{
		"cooldown": 40,
		"cost": 20,
		"target": true,
	}
}
var game: Game
var cooldown_timer: Timer
var is_active: bool = false
var is_on_cooldown: bool = false
var range_indicator: RangeIndicator


func _ready() -> void:
	game = get_parent() as Game
	range_indicator = get_node("Range")
	create_timers()


func create_timers():
	# Create cooldown timer
	cooldown_timer = Timer.new()
	cooldown_timer.one_shot = true
	cooldown_timer.timeout.connect(_on_cooldown_ended)
	add_child(cooldown_timer)


func cast_spell(cell_pos: Vector2i) -> bool:
	if is_on_cooldown or is_active or not game:
		print("Spell is on cooldown! Wait ", cooldown_timer.get_time_left(), " seconds")
		return false
	if not game.spend(metadata.stats.cost):
		print("Not enough money")
		return false
	activate_effect(cell_pos)
	return true


func activate_effect(cell_pos: Vector2i):
	print("Current cell_pos:", cell_pos)
	is_active = true
	var stats = metadata.stats

	# Start timers
	cooldown_timer.wait_time = stats.cooldown
	cooldown_timer.start()


func _on_cooldown_ended():
	is_on_cooldown = false
	print("Double income spell ready to cast again!")
