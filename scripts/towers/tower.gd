class_name Tower
extends Area2D

@export var building_cost: int = 50
@export var upgrade_cost: int = 10
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
var reload_timer: Timer


func _ready():
	add_to_group("towers")
	enabled = false
	reload_timer = Timer.new()
	self.add_child(reload_timer)
	reload_timer.timeout.connect(self._on_reload_timer_timeout)


func enable(_global_position: Vector2) -> void:
	enabled = true
	global_position = _global_position
	reload_timer.start(reload_seconds)


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


func _move_toward_angle(from: float, to: float, max_delta: float) -> float:
	var angle_diff = wrapf(to - from, -PI, PI)
	angle_diff = clamp(angle_diff, -max_delta, max_delta)
	return from + angle_diff


func _physics_process(_delta: float) -> void:
	if not enabled:
		return
	_refresh_target()


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		return
	var origin: Vector2 = self.global_position
	var direction: float = (target.global_position - origin).angle()
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target)


func to_dict(coord: Vector2i) -> Dictionary:
	var dict: Dictionary = {}
	dict["type"] = 0
	dict["position"] = {"x": coord[0], "y": coord[1]}
	dict["level"] = 1
	dict["aim"] = "what"
	dict["anti_air"] = anti_air
	dict["bullet_number"] = bullet_number
	dict["reload"] = reload_seconds
	dict["range"] = aim_range
	dict["damage"] = damage
	return dict
