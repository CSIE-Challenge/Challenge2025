class_name Bullet
extends Area2D

const RANGE_ATTACK_ANIMATION_TIME := 0.075

@export var is_tracking: bool = true
@export var is_anti_air: bool = false
@export var is_penetrating: bool = false
@export var aoe_scale: float = 1
@export var shockwave_scene: PackedScene
@export var movement_speed := 400.0
@export var rotation_speed := 8.0
@export var damage := 3
@export var lifespan_seconds := 5
@export var effect_damage := 2
@export var effect_duration := 3
@export var effect_interval := 0.5

var target: Node2D = null
var start_position: Vector2
var alive: bool = true  # make sure each bullet deals damage once
var timer = Timer.new()
var effect_timer = Timer.new()
var respawn_effect_timer = Timer.new()
var exploding: bool = false  # bullet explode after time_out if AOE > 0

@onready var collider := $CollisionShape2D


func init(origin, orientation, _target) -> void:
	AudioManager.tower_shoot.play()
	global_position = origin
	start_position = origin
	rotation = orientation
	target = _target

	# Shockwave damage only when explosion done
	if lifespan_seconds == 0:
		_explode()
	self.add_child(timer)
	self.add_child(effect_timer)
	self.add_child(respawn_effect_timer)
	timer.timeout.connect(destroy, CONNECT_ONE_SHOT)
	effect_timer.timeout.connect(_on_effect_end, CONNECT_ONE_SHOT)
	respawn_effect_timer.timeout.connect(_on_respawn)
	timer.start(lifespan_seconds)


func _process(delta):
	if exploding:
		return

	var desired_angle: float

	if target == null or not is_instance_valid(target) or not is_tracking:
		desired_angle = rotation
	else:
		desired_angle = (target.global_position - global_position).angle()

	rotation = lerp_angle(rotation, desired_angle, rotation_speed * delta)
	position += Vector2.RIGHT.rotated(rotation) * movement_speed * delta

	var traverse_distance = global_position.distance_to(start_position)

	# The bullet must be above the tower after it is fired
	if traverse_distance >= 10.0 and not exploding:
		self.z_index = 20


func destroy() -> void:
	timer.stop()
	if aoe_scale == 1:  # Normal bullet
		self.queue_free()
	elif aoe_scale == 0:  # Generate a shockwave
		var shockwave := shockwave_scene.instantiate()
		self.get_parent().add_child(shockwave)
		shockwave.init(global_position, rotation, null)
		self.queue_free()
	else:  # Shockwave that expand
		_explode()


func _explode() -> void:
	exploding = true
	self.z_index = 0
	var tween = create_tween()
	tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
	tween.set_ease(Tween.EASE_OUT)
	tween.finished.connect(_on_exploded, CONNECT_ONE_SHOT)
	tween.tween_property(self, "scale", Vector2(aoe_scale, aoe_scale), RANGE_ATTACK_ANIMATION_TIME)


func _on_exploded() -> void:
	if effect_duration == 0:
		_on_effect_end()
	collider.disabled = true
	print("on_exploded")
	damage = effect_damage
	respawn_effect_timer.start(effect_interval / 2.0)
	effect_timer.start(effect_duration)


func _on_respawn() -> void:
	print("on_respawn")
	collider.disabled = !collider.disabled


func _on_effect_end() -> void:
	respawn_effect_timer.stop()
	print("on_effect_end")
	self.queue_free()
