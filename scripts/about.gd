extends Control


func _ready():
	$Quit.grab_focus()


func _on_quit_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/menu.tscn")
