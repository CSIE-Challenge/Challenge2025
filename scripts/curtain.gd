extends Label
var speed = 150.0


func _process(delta):
	position.x -= speed * delta
	if position.x + size.x < 0:
		queue_free()


func setup(text: String, font_size := 24, color := Color.WHITE):
	self.text = text
	var font = FontFile.new()
	add_theme_font_size_override("font_size", font_size)
	add_theme_color_override("font_color", color)
