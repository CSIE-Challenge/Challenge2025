extends Control

@onready var setting_submenu = $Settings


func pause():
	get_tree().paused = true
	AudioManager.button_on_click.play()
	if AudioManager.second_stage:
		AudioManager.background2_music_position = (
			AudioManager.background_game_stage2.get_playback_position()
		)
		AudioManager.background_game_stage2.stop()
	else:
		AudioManager.background1_music_position = (
			AudioManager.background_game_stage1.get_playback_position()
		)
		AudioManager.background_game_stage1.stop()
	self.visible = true


func resume():
	if setting_submenu.visible:
		setting_submenu.close()
		_on_settings_exit()
	get_tree().paused = false
	AudioManager.button_on_click.play()
	if AudioManager.second_stage:
		AudioManager.background_game_stage2.play(AudioManager.background2_music_position)
	else:
		AudioManager.background_game_stage1.play(AudioManager.background1_music_position)
	self.visible = false


func _ready():
	self.visible = false
	setting_submenu.exit_button_pressed.connect(_on_settings_exit)


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
	AudioManager.button_on_click.play()
	$PauseMenu.visible = false

	setting_submenu.open()


func _on_settings_exit() -> void:
	AudioManager.button_on_click.play()
	$PauseMenu.visible = true
