extends Control

const SQUARE_SIZE = Vector2(50, 50)

var squares = []


func _ready():
	var challenge_label = $ChallengeLabel
	var challenge_text = challenge_label.text
	var map_label = $MapLabel
	var map_text = map_label.text
	challenge_label.text = ""
	map_label.text = ""
	create_tween().tween_property(challenge_label, "text", challenge_text, 1.0).set_delay(1.0)
	create_tween().tween_property(map_label, "text", map_text, 1.0).set_delay(3.0)
	for x in range(-25, 750, 50):
		for y in range(-25, 1000, 50):
			var square = ColorRect.new()
			square.size = SQUARE_SIZE
			square.color = Color.GREEN
			square.modulate.a = 0.0  # Start invisible
			square.position = Vector2(x, y)

			add_child(square)
			squares.push_back(square)

			# Tween fade-in

			var tween = create_tween()
			var delay = max(randf_range(0.0, 3.0), randf_range(0.0, 3.0))
			var duration = 0.1
			tween.tween_property(square, "modulate:a", 1.0, duration).set_delay(delay + 5.0)


func clear_square():
	for square in squares:
		square.queue_free()
