extends Node2D

@onready var chat_input = $ChatInput
@onready var message_box = $MessageBox


func _on_send_button_pressed() -> void:
	message_box.text += str("P: ", chat_input.text, "\n")
	chat_input.text = ""
	message_box.scroll_vertical = message_box.get_line_count() - 1
