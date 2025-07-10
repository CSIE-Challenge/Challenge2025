class_name TowerUi
extends Control

signal sold


# the tower's UI intercepts input events before GUI (because it is impossible to trigger both)
func _input(event):
	if (
		event is InputEventMouseButton
		and event.button_index == MOUSE_BUTTON_LEFT
		and event.pressed
		and not get_global_rect().has_point(get_global_mouse_position())
	):
		queue_free()
		get_viewport().set_input_as_handled()


func _on_sell_button_pressed() -> void:
	sold.emit()
