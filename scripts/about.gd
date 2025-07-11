extends Control


func _ready():
	$Quit.grab_focus()


func _on_quit_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/menu.tscn")
