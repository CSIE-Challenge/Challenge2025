extends Control

signal upgrade_button_pressed;
signal sell_button_pressed;

var selected_tower: Tower = null


func _ready():
	visible = false


func _unhandled_input(event):
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed:
		if not get_rect().has_point(get_local_mouse_position()):
			visible = false
			get_viewport().set_input_as_handled()


func _on_upgrade_button_pressed() -> void:
	upgrade_button_pressed.emit(selected_tower)


func _on_sell_button_pressed() -> void:
	sell_button_pressed.emit(selected_tower)
	visible = false
	selected_tower = null


func on_tower_selected(tower: Tower) -> void:
	global_position = tower.global_position
	selected_tower = tower
	visible = true
