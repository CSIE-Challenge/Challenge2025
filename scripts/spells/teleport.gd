class_name TeleportSpell
extends Node
static var metadata: Dictionary = {
	"name": "DoubleIncome",
	"scene_path": "res://scenes/spells/teleport.tscn",
	"description": "I am rich",
	"stats":
	{
		"duration": 20,
		"cooldown": 40,
		"cost": 20,
	}
}
var game: Game
var duration_timer: Timer
var cooldown_timer: Timer
var is_active: bool = false
var is_on_cooldown: bool = false
