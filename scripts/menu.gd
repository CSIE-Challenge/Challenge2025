extends Control


func _ready():
	$VBoxContainer/Start.grab_focus()


func _on_start_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/ui.tscn")


func _on_about_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/about.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
