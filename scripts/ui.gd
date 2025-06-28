extends Node2D

@onready var chat_input = $Message/ChatInput
@onready var message_box = $Message/MessageBox


func _on_chat_input_text_submitted(new_text: String) -> void:
	message_box.text += str("P: ", new_text, "\n")
	chat_input.text = ""
	message_box.scroll_vertical = message_box.get_line_count() - 1
	chat_input.grab_focus()


func _on_send_button_pressed() -> void:
	_on_chat_input_text_submitted(chat_input.text)
