class_name TwinTurret
extends Tower

var current_shoot_turret: int = 0  # 0 for left, 1 for right

@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


# take aim when enabled
func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - turret.global_position).angle()
		turret.rotation = _move_toward_angle(turret.rotation, desired_angle)
	return


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		return

	var origin: Vector2
	var orientation = $Turret.rotation

	origin = Vector2(0, 0)
	if current_shoot_turret == 0:
		origin = $Turret/Left.global_position
		current_shoot_turret = 1
	else:
		origin = $Turret/Right.global_position
		current_shoot_turret = 0

	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, orientation, target)
