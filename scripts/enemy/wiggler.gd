extends Enemy


func _ready() -> void:
	super._ready()
	var use_zhaobu = randf() < 0.1
	if use_zhaobu:
		$AnimatedSprite2D.play("new_animation")
