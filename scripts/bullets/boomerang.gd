class_name Boomerang
extends Bullet

# The acceleration of bullet back toward the tower
const RESISTENCE: float = 1000


func _process(delta):
	if exploding:
		return

	rotation += spanning_speed
	movement_speed -= RESISTENCE * delta
	position += Vector2.RIGHT.rotated(direction) * delta * movement_speed

	var traverse_distance = global_position.distance_to(start_position)

	# The bullet must be above the tower after it is fired
	if traverse_distance >= 10.0 and not exploding:
		self.z_index = 20
	if traverse_distance <= 10.0 and movement_speed < 0:
		self.destroy()
