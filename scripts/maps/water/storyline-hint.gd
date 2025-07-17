extends Control

@onready var copy_timer = $Timer
@onready var textbox = $StorylineContainer/MarginContainer/VBoxContainer/Message/Text
@onready var copy_button = $StorylineContainer/MarginContainer/VBoxContainer/Buttons/Copy


func _notification(what):
	if what == NOTIFICATION_PAUSED:
		self.visible = false
	elif what == NOTIFICATION_UNPAUSED:
		self.visible = true


func _on_copy_timer_timeout() -> void:
	copy_button.text = "Copy"


func _on_copy_pressed() -> void:
	copy_timer.stop()
	copy_timer.start()
	copy_button.text = "Copied!"
	DisplayServer.clipboard_set(textbox.text)


func _on_close_pressed() -> void:
	queue_free()


func _on_window_timer_timeout() -> void:
	queue_free()
