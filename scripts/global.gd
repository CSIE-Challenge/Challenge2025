extends Node


func _input(event):
	if event is InputEventKey and event.pressed and event.keycode == KEY_F11:
		var full = DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN
		DisplayServer.window_set_mode(
			DisplayServer.WINDOW_MODE_WINDOWED if full else DisplayServer.WINDOW_MODE_FULLSCREEN
		)
