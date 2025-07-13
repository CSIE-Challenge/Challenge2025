extends PanelContainer

var settings = ConfigFile.new()

@onready var master_slider = $MarginContainer/VBoxContainer2/VBoxContainer/Master
@onready var music_slider = $MarginContainer/VBoxContainer2/VBoxContainer/Music
@onready var sfx_slider = $MarginContainer/VBoxContainer2/VBoxContainer/SFX


func load_settings() -> void:
	settings.load("user://settings.cfg")
	master_slider.value = settings.get_value("Volume", "master", 1.0)
	music_slider.value = settings.get_value("Volume", "music", 1.0)
	sfx_slider.value = settings.get_value("Volume", "sfx", 1.0)


func _on_back_pressed() -> void:
	settings.set_value("Volume", "master", master_slider.value)
	settings.set_value("Volume", "music", music_slider.value)
	settings.set_value("Volume", "sfx", sfx_slider.value)
	settings.save("user://settings.cfg")
