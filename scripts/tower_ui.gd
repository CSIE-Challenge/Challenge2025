extends Control


func _ready():
	visible = false


func _unhandled_input(event):
	if not visible:
		return
	if event is InputEventMouseButton and event.pressed:
		if not get_rect().has_point(get_local_mouse_position()):
			visible = false
			get_viewport().set_input_as_handled()
