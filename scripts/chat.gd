extends TextureRect

const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")


func _on_line_edit_text_submitted(text: String) -> void:
	var textbox: MarginContainer = TEXTBOX_SCENE.instantiate()
	textbox.set_text(text)
	$MarginContainer/ScrollContainer/VBoxContainer.add_child(textbox)
	$LineEdit.clear()


func _on_switch_pressed() -> void:
	self.visible = false


func get_history(num: int) -> Array:
	var container = $MarginContainer/ScrollContainer/VBoxContainer
	var msgs: Array = []
	var all_msgs: Array = container.get_children()
	var count = min(num, all_msgs.size())
	for i in range(1, count):
		var box = all_msgs[-i]
		var label = box.get_node("MarginContainer/RichTextLabel")
		msgs.append(label.text)

	return msgs
