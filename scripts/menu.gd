extends Control


func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/player_selection/player_selection.tscn")


func _on_about_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/about.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
