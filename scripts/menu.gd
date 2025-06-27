extends Control


func _ready():
	$VBoxContainer/Start.grab_focus()


func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/game.tscn")


func _on_about_pressed() -> void:
	pass  # Replace with function body.


func _on_quit_pressed() -> void:
	get_tree().quit()
