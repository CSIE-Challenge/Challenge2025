extends TabBar

const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")


func _on_line_edit_text_submitted(text: String) -> void:
	var textbox: MarginContainer = TEXTBOX_SCENE.instantiate()
	textbox.set_text(text)
	$MarginContainer/ScrollContainer/VBoxContainer.add_child(textbox)
	$LineEdit.clear()
