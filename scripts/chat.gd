extends TextureRect

const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")

var always_visible: bool = false


func send_chat_with_sender(
	sender_id: int, chat_name_color: String, player_name: String, text: String
) -> void:
	var textbox: MarginContainer = TEXTBOX_SCENE.instantiate()

	if sender_id == 0:
		textbox.set_text(text)
	elif chat_name_color == "hyper":
		textbox.set_text(
			"[rainbow freq=1.0 sat=0.8 val=0.8 speed=0.3][%s][/rainbow]: %s" % [player_name, text]
		)
	else:
		textbox.set_text("[color=%s][%s][/color]: %s" % [chat_name_color, player_name, text])
	textbox.set_meta("sender", sender_id)

	$MarginContainer/ScrollContainer/VBoxContainer.add_child(textbox)


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
