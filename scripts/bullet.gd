extends Area2D

@export var speed := 400.0
@export var rotation_speed := 3.0
@export var max_distance := 800.0
@export var damage := 3

var target: Node2D = null
var start_position: Vector2


func _ready() -> void:
	start_position = global_position
	body_entered.connect(Callable(self, "_on_body_entered"))


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


func _on_body_entered(body: Node2D) -> void:
	body.take_damage(damage)
	# print("Bullet Hit: ", body.name)
	queue_free()
