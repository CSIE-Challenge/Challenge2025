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

	var bg = StyleBoxFlat.new()
	bg.bg_color = Color(0, 0, 0, 0.4)
	bg.corner_radius_top_left = 6
	bg.corner_radius_top_right = 6
	bg.corner_radius_bottom_left = 6
	bg.corner_radius_bottom_right = 6

	bg.content_margin_left = 8
	bg.content_margin_right = 8
	bg.content_margin_top = 4
	bg.content_margin_bottom = 4

	add_theme_stylebox_override("normal", bg)
	await self.ready
	self.size = self.get_minimum_size()
