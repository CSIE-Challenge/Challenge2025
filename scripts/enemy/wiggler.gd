extends Enemy


func _ready() -> void:
	var use_zhaobu = randf() < 0.1
	if use_zhaobu:
		$AnimatedSprite2D.play("new_animation")
