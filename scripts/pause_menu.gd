extends Control


func pause():
	get_tree().paused = true
	self.visible = true


func resume():
	get_tree().paused = false
	self.visible = false


func _ready():
	self.visible = false


func _process(_delta):
	if Input.is_action_just_pressed("Pause"):
		if get_tree().paused:
			resume()
		else:
			pause()


func _on_resume_pressed() -> void:
	resume()


func _on_exit_pressed() -> void:
	get_tree().quit()


func _on_settings_pressed() -> void:
	$PauseMenu.visible = false
	$Settings.load_settings()
	$Settings.visible = true


func _on_back_pressed() -> void:
	$PauseMenu.visible = true
	$Settings.visible = false
