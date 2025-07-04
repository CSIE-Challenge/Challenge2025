class_name Tower
extends Area2D


@export var level: int = 1
@export var auto_aim: bool = true
@export var anti_air: bool = false
@export var bullet_scene: PackedScene
@export var bullet_number: int = 1
@export var reload_seconds: float = 0.25
@export var aim_range: float = 450
@export var damage: int = 2
@export var rotation_speed: float = 90.0  # degree per second


var target: Node2D = null
var enabled: bool = false
var current_shoot_turret: int = 0  # 0 for left, 1 for right


@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D
@onready var reload_timer = $ReloadTimer


func enable(_global_position: Vector2) -> void:
	enabled = true
	global_position = _global_position
	reload_timer.start()


func _ready():
	enabled = false
	enemy_detector.shape.radius = 0.5 * aim_range
	reload_timer.wait_time = reload_seconds
	add_to_group("towers")


func _refresh_target():
	if target != null and is_instance_valid(target) and self.overlaps_area(target):
		return
	target = null
	var enemies: Array[Area2D] = $AimRange.get_overlapping_areas()
	if enemies.size() == 0:
		return
	target = enemies[0]
	var closest_distance = position.distance_to(target.position)
	for i in range(1, enemies.size()):
		var distance = position.distance_to(enemies[i].position)
		if distance < closest_distance:
			target = enemies[i]
			closest_distance = distance


func move_toward_angle(from: float, to: float, max_delta: float) -> float:
	var angle_diff = wrapf(to - from, -PI, PI)
	angle_diff = clamp(angle_diff, -max_delta, max_delta)
	return from + angle_diff


func _physics_process(delta: float) -> void:
	if not enabled:
		return
	_refresh_target()
	# take aim
	if target != null:
		var desired_angle = (target.global_position - turret.global_position).angle()
		var max_rotation = deg_to_rad(rotation_speed) * delta
		turret.rotation = move_toward_angle(turret.rotation, desired_angle, max_rotation)


func shoot() -> void:
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
	damage += 1
	aim_range += 100
	reload_seconds = 60.0 / (60.0 / reload_seconds + 60)
	rotation_speed += 20
	enemy_detector.shape.radius = 0.5 * aim_range
	reload_timer.wait_time = reload_seconds
