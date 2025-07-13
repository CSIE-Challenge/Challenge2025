extends Node2D


func _process(_delta):
	if position.y > get_viewport_rect().size.y + 50:
		queue_free()
