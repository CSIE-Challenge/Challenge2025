class_name TowerWithSingleBullet
extends Tower

@onready var marker = $Tower/Marker2D


func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		sprite.flip_h = cos(desired_angle) < 0
		if sprite.flip_h:
			marker.position.x = -abs(marker.position.x)
		else:
			marker.position.x = abs(marker.position.x)
