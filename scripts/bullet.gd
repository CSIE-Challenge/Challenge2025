class_name Bullet
extends Area2D

@export var speed := 400.0
@export var rotation_speed := 30.0
@export var max_distance := 800.0
@export var damage := 3

var target: Node2D = null
var start_position: Vector2
var alive: bool = true


func init(origin, orientation, _target) -> void:
	global_position = origin
	start_position = origin
	rotation = orientation
	target = _target


func _process(delta):
	if target == null or not is_instance_valid(target):
		queue_free()
		return

	var dir = (target.global_position - global_position).normalized()
	var desired_angle = dir.angle()

	rotation = lerp_angle(rotation, desired_angle, rotation_speed * delta)
	position += Vector2.RIGHT.rotated(rotation) * speed * delta

	var traverse_distance = global_position.distance_to(start_position)

	# The bullet must be above the tower after it is fired
	if traverse_distance >= 10.0:
		self.z_index = 20

	if traverse_distance >= max_distance:
		queue_free()
