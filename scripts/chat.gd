extends TextureRect

const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")

var always_visible: bool = false


func send_chat_with_sender(sender_id: int, text: String) -> void:
	var textbox: MarginContainer = TEXTBOX_SCENE.instantiate()
	textbox.set_text(text)
	textbox.set_meta("sender", sender_id)
	$MarginContainer/ScrollContainer/VBoxContainer.add_child(textbox)
	$LineEdit.clear()


func _on_line_edit_text_submitted(text: String) -> void:
	send_chat_with_sender(0, text)


func _on_switch_pressed() -> void:
    if not always_visible:
		self.visible = false


func get_history(num: int) -> Array:
	var container = $MarginContainer/ScrollContainer/VBoxContainer
	var msgs: Array = []
	var all_msgs: Array = container.get_children()
	var count = min(num, all_msgs.size())
	for i in range(1, count + 1):
		var box = all_msgs[-i]
		var sender_id = int(box.get_meta("sender"))
		var label = box.get_node("MarginContainer/RichTextLabel")
		msgs.append([sender_id, label.text])

	return msgs
