class_name TowerThrowingBullet
extends Tower

@onready var tower_body = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


# take aim when enabled
func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		tower_body.rotation = _get_sprite_direction(desired_angle)
