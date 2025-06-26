extends StaticBody2D

@export var bullet_scene: PackedScene

var damage: int = 2
var rotation_speed: float = 90.0  # degree per second
var aim_range: float = 450.0
var reload_speed: float = 240  # per minute
var level: int = 1
var current_shoot_turret: int = 0  # 0 for left, 1 for right

var enemies: Array = []

var target: Node2D = null
var targets = []

var built: bool = false
var is_preview := false

@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D
@onready var reload_timer = $ReloadTimer


func _ready():
	if is_preview:
		apply_preview_appearance()
		$Button.visible = false
	else:
		built = true
		enemy_detector.shape.radius = 0.5 * aim_range
		reload_timer.wait_time = 60.0 / reload_speed
		reload_timer.start()


func apply_preview_appearance():
	for child in get_children():
		if child is CanvasItem:
			child.modulate = Color(1, 1, 1, 0.5)
	set_process(false)


func _physics_process(delta: float) -> void:
	if enemies.size() > 0 and built:
		aim(delta)


func move_toward_angle(from: float, to: float, max_delta: float) -> float:
	var angle_diff = wrapf(to - from, -PI, PI)
	angle_diff = clamp(angle_diff, -max_delta, max_delta)
	return from + angle_diff


func aim(delta: float) -> void:
	if enemies.is_empty():
		return

	target = enemies[0]
	var desired_angle = (target.global_position - turret.global_position).angle()
	var max_rotation = deg_to_rad(rotation_speed) * delta

	turret.rotation = move_toward_angle(turret.rotation, desired_angle, max_rotation)


func _choose_target():
	target = null
	targets = $AimRange.get_overlapping_bodies()
	if targets.size() == 0:
		return

	var closest_target = targets[0]
	var closest_distance = position.distance_to(closest_target.position)
	for i in range(1, targets.size()):
		var distance = position.distance_to(targets[i].position)
		if distance < closest_distance:
			closest_target = targets[i]
			closest_distance = distance

	target = closest_target


func shoot() -> void:
	_choose_target()
	if target == null:
		return

	var bullet = bullet_scene.instantiate()

	if current_shoot_turret == 0:
		bullet.global_position = $Turret/Left.global_position
		current_shoot_turret = 1
	else:
		bullet.global_position = $Turret/Right.global_position
		current_shoot_turret = 0

	bullet.damage = damage
	bullet.rotation = $Turret.rotation
	bullet.target = target

	get_tree().current_scene.add_child(bullet)
	# print("Bullet fired at target: ", target.name)


func _on_aim_range_body_entered(body: Node2D) -> void:
	if body == self:
		return
	enemies.append(body.get_parent())


func _on_aim_range_body_exited(body: Node2D) -> void:
	enemies.erase(body.get_parent())


func _on_reload_timer_timeout() -> void:
	if enemies.size() > 0:
		shoot()
