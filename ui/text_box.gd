extends MarginContainer


func set_text(text: String):
	$MarginContainer/RichTextLabel.text = text
	if "I use Arch, btw." in text:
		$MarginContainer/LinkButton.set_uri("https://wiki.archlinux.org/title/Main_page")
	elif "Ruby 醬，嗨，你喜歡什麼？" in text:
		$MarginContainer/LinkButton.set_uri("https://www.instagram.com/reel/DI00i2FSkfj/")
	elif "d_ouo_b_" in text:
		$MarginContainer/LinkButton.set_uri("https://www.instagram.com/\
d_ouo_b_?igsh=MWcyenNwZjNibGI4dA%3D%3D&utm_source=qr")


func set_line_height(send_pixelcat: bool):
	if send_pixelcat:
		$MarginContainer/RichTextLabel.add_theme_constant_override("line_separation", 2)
