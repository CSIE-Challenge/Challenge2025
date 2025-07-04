class_name TwinTurret
extends Tower


var current_shoot_turret: int = 0  # 0 for left, 1 for right


@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


# take aim when enabled
func _physics_process(delta: float) -> void:
	if not enabled:
		return
	_refresh_target()
	if target != null:
		var desired_angle = (target.global_position - turret.global_position).angle()
		var max_rotation = deg_to_rad(rotation_speed) * delta
		turret.rotation = _move_toward_angle(turret.rotation, desired_angle, max_rotation)


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


func upgrade() -> void:
	upgrade_cost += 10
	damage += 1
	aim_range += 100
	reload_seconds = 60.0 / (60.0 / reload_seconds + 60)
	rotation_speed += 20
	enemy_detector.shape.radius = 0.5 * aim_range
	reload_timer.wait_time = reload_seconds
