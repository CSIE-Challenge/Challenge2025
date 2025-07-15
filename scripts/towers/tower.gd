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
var has_cooldowned: bool = false
var reload_timer: Timer
var wait_for_animation_timer: Timer
var strategy: TargetStrategy = TargetStrategy.FIRST
var bullet_effect: String  # only used in to_dict

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var enemy_detector = $AimRange/CollisionShape2D
@onready var anime = $Tower/AnimatedSprite2D


func _ready():
	add_to_group("towers")
	self.z_index = 10  # For effect to be on the ground
	enemy_detector.shape.radius = 0.5 * aim_range
	bullet_effect = bullet_scene.instantiate().get_effect_name()
	# Initialize timers
	reload_timer = Timer.new()
	wait_for_animation_timer = Timer.new()
	reload_timer.one_shot = true
	wait_for_animation_timer.one_shot = true
	self.add_child(reload_timer)
	self.add_child(wait_for_animation_timer)
	reload_timer.timeout.connect(self._on_reload_timer_timeout)
	wait_for_animation_timer.timeout.connect(self._on_fire_bullet)


# Take in the map so the the fort can decide which direction to face
func enable(_global_position: Vector2, _map: Map) -> void:
	enabled = true
	has_cooldowned = true
	global_position = _global_position
	AudioManager.tower_place.play()


func set_strategy(new_strategy: TargetStrategy) -> void:
	strategy = new_strategy


func _refresh_target() -> void:
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


# Abstract
func _flip_sprite() -> void:
	return


func _physics_process(_delta: float) -> void:
	if not enabled:
		return


func _on_aim_range_area_entered(_area: Area2D) -> void:
	if has_cooldowned:
		_on_reload_timer_timeout()


func _on_reload_timer_timeout() -> void:
	has_cooldowned = false
	_refresh_target()
	if target == null:
		has_cooldowned = true
		return
	reload_timer.start(reload_seconds)
	_flip_sprite()
	if not anime.is_playing():
		anime.play("default")
	var attack_scene = sprite.sprite_frames.get_frame_count(sprite.animation) - 2
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION * attack_scene)


func _on_fire_bullet() -> void:
	if not (target != null and is_instance_valid(target)):
		_refresh_target()
		if target == null:
			has_cooldowned = true
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
