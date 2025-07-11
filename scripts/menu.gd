extends Control


func _ready() -> void:
	AudioManager.background_menu.play()


func _on_start_pressed() -> void:
	AudioManager.button_on_click.play()
	AudioManager.background_menu.stop()
	$Version.text = "v%s" % [ProjectSettings.get_setting("application/config/version")]
	get_tree().change_scene_to_file("res://scenes/player_selection/player_selection.tscn")


func _on_about_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/about.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()
