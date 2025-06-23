extends Control

func _ready():
	visible = false


func _on_button_pressed() -> void:
	global_position = get_parent().global_position
	visible = true

func _input(event):
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed:
		var mouse_pos = get_global_mouse_position()
		if not get_global_rect().has_point(mouse_pos):
			visible = false
			get_viewport().set_input_as_handled()
