extends MarginContainer


func set_text(text: String):
	$MarginContainer/RichTextLabel.text = text


func set_line_height(send_pixelcat: bool):
	if send_pixelcat:
		$MarginContainer/RichTextLabel.add_theme_constant_override("line_separation", 2)
