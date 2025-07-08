class_name Tower
extends Area2D

enum TargetStrategy { FIRST, LAST, CLOSE }

@export var building_cost: int = 5
@export var upgrade_cost: int = 10
@export var auto_aim: bool = true
@export var anti_air: bool = false
@export var bullet_scene: PackedScene
@export var reload_seconds: float = 0.25
@export var aim_range: float = 450
@export var damage: int = 2
# Should be a variable controlled otherwise later
@export var strategy: TargetStrategy = TargetStrategy.FIRST
var target: Node2D = null
var enabled: bool = false
var reload_timer: Timer

@onready var anime = $Turret/AnimatedSprite2D


func _ready():
	add_to_group("towers")
	enabled = false
	reload_timer = Timer.new()
	self.add_child(reload_timer)
	reload_timer.timeout.connect(self._on_reload_timer_timeout)
	self.z_index = 10  # For effect to be on the ground


# Take in the map so the the fort can decide which direction to face
func enable(_global_position: Vector2, _map: Map) -> void:
	enabled = true
	global_position = _global_position
	reload_timer.start(reload_seconds)
	AudioManager.tower_place.play()


func _refresh_target() -> void:
	if target != null and is_instance_valid(target) and self.overlaps_area(target):
		return
	target = null
	var enemies: Array[Area2D] = $AimRange.get_overlapping_areas()

	if enemies.is_empty():
		return
	target = enemies[0]

	match strategy:
		TargetStrategy.CLOSE:
			var closest_distance = position.distance_to(target.position)
			for i in range(1, enemies.size()):
				var distance = position.distance_to(enemies[i].position)
				if distance < closest_distance:
					target = enemies[i]
					closest_distance = distance
		TargetStrategy.FIRST:
			var largest_progress = target.path_follow.progress_ratio
			for i in range(1, enemies.size()):
				var progress = enemies[i].path_follow.progress_ratio
				if progress > largest_progress:
					target = enemies[i]
					largest_progress = progress
		TargetStrategy.LAST:
			var smallest_progress = target.path_follow.progress_ratio
			for i in range(1, enemies.size()):
				var progress = enemies[i].path_follow.progress_ratio
				if progress < smallest_progress:
					target = enemies[i]
					smallest_progress = progress


# For default tower only (can be deleted later)
func _move_toward_angle(from: float, to: float, max_delta: float = PI / 15) -> float:
	var angle_diff = wrapf(to - from, -PI, PI)
	angle_diff = clamp(angle_diff, -max_delta, max_delta)
	return from + angle_diff


# Inherited class can make the sprites to face either left or right
func _flip_sprite() -> void:
	return


func _get_sprite_direction(angle: float) -> bool:
	angle = wrapf(angle, -PI, PI)
	if angle <= PI / 2 and angle >= -PI / 2:
		return false
	return true


func _physics_process(_delta: float) -> void:
	if not enabled:
		return
	_refresh_target()
	_flip_sprite()


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		anime.stop()
		return
	if not anime.is_playing():
		anime.play("default")
	var origin: Vector2 = self.global_position
	var direction: float = (target.global_position - origin).angle()
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target)
