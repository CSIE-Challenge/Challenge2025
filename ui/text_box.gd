extends MarginContainer


func set_text(text: String):
	$MarginContainer/RichTextLabel.text = text
	if "I use Arch, btw." in text:
		$MarginContainer/LinkButton.set_uri("https://wiki.archlinux.org/title/Main_page")


func _on_link_button_pressed() -> void:
	print($MarginContainer/LinkButton.uri)

	#match $MarginContainer/RichTextLabel.text:
	#"I use Arch, btw."
