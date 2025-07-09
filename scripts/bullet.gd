class_name Bullet
extends Area2D

@export var is_tracking: bool = false
@export var is_anti_air: bool = false
@export var is_penetrating: bool = false
@export var aoe_radius: float = 0
@export var movement_speed := 400.0
@export var rotation_speed := 3.0
@export var damage := 3
@export var lifespan_seconds := 5

var target: Node2D = null
var start_position: Vector2
var alive: bool = true  # make sure each bullet deals damage once
var timer = Timer.new()


func init(origin, orientation, _target) -> void:
	AudioManager.tower_shoot.play()
	global_position = origin
	start_position = origin
	rotation = orientation
	target = _target

	self.add_child(timer)
	timer.timeout.connect(self.queue_free)
	timer.start(lifespan_seconds)


func _process(delta):
	var desired_angle: float

	if target == null or not is_instance_valid(target):
		desired_angle = rotation
	else:
		desired_angle = (target.global_position - global_position).angle()

	rotation = lerp_angle(rotation, desired_angle, rotation_speed * delta)
	position += Vector2.RIGHT.rotated(rotation) * movement_speed * delta

	var traverse_distance = global_position.distance_to(start_position)

	# The bullet must be above the tower after it is fired
	if traverse_distance >= 10.0:
		self.z_index = 20
