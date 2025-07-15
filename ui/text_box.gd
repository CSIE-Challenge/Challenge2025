extends MarginContainer


func set_text(text: String):
	$MarginContainer/RichTextLabel.text = text
	#$MarginContainer/LinkButton.set_uri("https://wiki.archlinux.org/title/Main_page")
	if "I use Arch, btw." in text:
		$MarginContainer/LinkButton.set_uri("https://wiki.archlinux.org/title/Main_page")
	elif "Ruby 醬，嗨，你喜歡什麼？" in text:
		$MarginContainer/LinkButton.set_uri("https://www.instagram.com/reel/DI00i2FSkfj/")
