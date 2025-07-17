extends PanelContainer

signal exit_button_pressed

var settings = ConfigFile.new()

@onready var master_slider = $MarginContainer/VBoxContainer2/VBoxContainer/Master
@onready var music_slider = $MarginContainer/VBoxContainer2/VBoxContainer/Music
@onready var sfx_slider = $MarginContainer/VBoxContainer2/VBoxContainer/SFX


func _ready() -> void:
	exit_button_pressed.connect(_on_exit_button_pressed)


func open() -> void:
	settings.load("user://settings.cfg")
	master_slider.value = settings.get_value("Volume", "master", 1.0)
	music_slider.value = settings.get_value("Volume", "music", 1.0)
	sfx_slider.value = settings.get_value("Volume", "sfx", 1.0)
	self.visible = true


func close() -> void:
	settings.set_value("Volume", "master", master_slider.value)
	settings.set_value("Volume", "music", music_slider.value)
	settings.set_value("Volume", "sfx", sfx_slider.value)
	settings.save("user://settings.cfg")
	self.visible = false


func _on_exit_button_pressed() -> void:
	AudioManager.button_on_click.play()
	close()


func _on_back_pressed() -> void:
	AudioManager.button_on_click.play()
	exit_button_pressed.emit()
