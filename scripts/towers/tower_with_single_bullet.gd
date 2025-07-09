class_name TowerWithSingleBullet
extends Tower

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var marker = $Tower/Marker2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		sprite.flip_h = cos(desired_angle) < 0
		if sprite.flip_h:
			marker.position.x = -abs(marker.position.x)
		else:
			marker.position.x = abs(marker.position.x)
