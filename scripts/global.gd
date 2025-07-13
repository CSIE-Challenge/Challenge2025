extends Node

var settings = ConfigFile.new()


func _ready() -> void:
	settings.load("user://settings.cfg")

	var master_volume = settings.get_value("Volume", "master", 1.0)
	var music_volume = settings.get_value("Volume", "music", 1.0)
	var sfx_volume = settings.get_value("Volume", "sfx", 1.0)

	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), linear_to_db(master_volume))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Music"), linear_to_db(music_volume))
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("SFX"), linear_to_db(sfx_volume))


func _input(event):
	if event is InputEventKey and event.pressed and event.keycode == KEY_F11:
		var full = DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN
		DisplayServer.window_set_mode(
			DisplayServer.WINDOW_MODE_WINDOWED if full else DisplayServer.WINDOW_MODE_FULLSCREEN
		)
