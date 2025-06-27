extends Control

var selected_tower: Tower = null
var game: Game = null


func _ready():
	visible = false


func _unhandled_input(event):
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed:
		if not get_rect().has_point(get_local_mouse_position()):
			visible = false
			get_viewport().set_input_as_handled()


func _on_tower_upgrade_button_pressed() -> void:
	var levelup_cost: int = selected_tower.level * 10
	if game.money >= levelup_cost:
		game.money -= levelup_cost
		selected_tower.upgrade()
