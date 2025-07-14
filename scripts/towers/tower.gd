class_name Tower
extends Area2D

enum TargetStrategy { FIRST, LAST, CLOSE }
# NONE to compatible with twin_turret
enum TowerType { NONE, FIRE_MARIO, ICE_LUIGI, DONEKEY_KONG, FORT, SHY_GUY }

const ANIMATION_FRAME_DURATION := 0.1

@export var type: TowerType = TowerType.NONE
@export var level_a: int = 1
@export var level_b: int = 1
@export var building_cost: int = 5
@export var auto_aim: bool = true
@export var anti_air: bool = false
@export var bullet_scene: PackedScene
@export var reload_seconds: float = 1
@export var aim_range: float = 450
@export var damage: int = 2
var target: Node2D = null
var enabled: bool = false
var reload_timer: Timer
var wait_for_animation_timer: Timer
var strategy: TargetStrategy = TargetStrategy.FIRST
var bullet_effect: String  # only used in to_dict

@onready var anime = $Tower/AnimatedSprite2D


func _ready():
	add_to_group("towers")
	enabled = false
	reload_timer = Timer.new()
	wait_for_animation_timer = Timer.new()
	self.add_child(reload_timer)
	self.add_child(wait_for_animation_timer)
	reload_timer.timeout.connect(self._on_reload_timer_timeout)
	self.z_index = 10  # For effect to be on the ground
	bullet_effect = bullet_scene.instantiate().get_effect_name()


# Take in the map so the the fort can decide which direction to face
func enable(_global_position: Vector2, _map: Map) -> void:
	enabled = true
	global_position = _global_position
	reload_timer.start(reload_seconds)
	AudioManager.tower_place.play()


func set_strategy(new_strategy: TargetStrategy) -> void:
	strategy = new_strategy


func _check_enemy_state() -> void:
	if target != null and is_instance_valid(target) and self.overlaps_area(target):
		return
	target = null
	var enemies: Array[Area2D] = $AimRange.get_overlapping_areas()

	if enemies.is_empty():
		return
	target = enemies[0]


func _refresh_target() -> void:
	_check_enemy_state()
	if target == null:
		return
	var enemies: Array[Area2D] = $AimRange.get_overlapping_areas()

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


func _physics_process(_delta: float) -> void:
	if not enabled:
		return
	#_refresh_target()
	_flip_sprite()


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		return
	if not anime.is_playing():
		anime.play("default")
	wait_for_animation_timer.timeout.connect(self._on_fire_bullet, CONNECT_ONE_SHOT)
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION)


func _on_fire_bullet() -> void:
	_check_enemy_state()
	if target == null:
		_refresh_target()
	if target == null:
		return
	var origin: Vector2 = $Tower/Marker2D.global_position
	var direction: float = (target.global_position - origin).angle()
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target, damage)


func to_dict(coord: Vector2i) -> Dictionary:
	var dict: Dictionary = {}
	dict["type"] = type
	dict["position"] = {"x": coord[0], "y": coord[1]}
	dict["level_a"] = level_a
	dict["level_b"] = level_b
	dict["aim"] = auto_aim
	dict["anti_air"] = anti_air
	dict["reload"] = reload_seconds
	dict["range"] = aim_range
	dict["damage"] = damage
	dict["bullet_effect"] = bullet_effect
	return dict
