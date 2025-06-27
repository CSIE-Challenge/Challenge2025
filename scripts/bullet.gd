extends Area2D

@export var speed := 400.0
@export var rotation_speed := 3.0
@export var time_to_live := 5.0  # seconds
@export var damage := 3

var target: Node2D = null
var start_position: Vector2
var _start_time := 0.0


func _ready() -> void:
	start_position = global_position
	body_entered.connect(Callable(self, "_on_body_entered"))
	_start_time = Time.get_ticks_msec() / 1000.0  # Record start time in seconds


func _elapsed_time() -> float:
	return Time.get_ticks_msec() / 1000.0 - _start_time


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

	if _elapsed_time() >= time_to_live:
		queue_free()


func _on_body_entered(body: Node2D) -> void:
	print("Bullet travel time: %.3f seconds" % _elapsed_time())
	body.take_damage(damage)
	# print("Bullet Hit: ", body.name)
	queue_free()
