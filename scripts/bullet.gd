extends Area2D

@export var speed := 400.0
@export var rotation_speed := 3.0
@export var max_distance := 800.0
@export var damage := 3

# --- PID gains (tune these!) ---
@export var pid_kp := 2.5
@export var pid_ki := 1.0
@export var pid_kd := 2.0

# --- Internal PID state ---
var _pid_error_sum := 0.0
var _pid_last_error := 0.0

var target: Node2D = null
var start_position: Vector2

func _ready() -> void:
	start_position = global_position
	_pid_error_sum = 0.0
	_pid_last_error = 0.0
	body_entered.connect(Callable(self, "_on_body_entered"))

func _process(delta):
	# check if the target is still valid
	if target == null or not is_instance_valid(target):
		queue_free()
		return

	# main logic for bullet movement
	_process_bullet_movement(delta)

	var traverse_distance = global_position.distance_to(start_position)

	# The bullet must be above the tower after it is fired
	if traverse_distance >= 10.0: # 10 pixels
		self.z_index = 20

	# Check if the bullet has traveled beyond the maximum distance
	if traverse_distance >= max_distance:
		queue_free()

func _process_bullet_movement(delta: float) -> void:
	# 1. Compute current heading error
	var dir = (target.global_position - global_position).normalized()
	var desired_angle = dir.angle()
	# wrap error to [-PI,PI]
	var error = wrapf(desired_angle - rotation, -PI, PI)

	# 2. PID terms
	_pid_error_sum += error * delta
	var derivative = (error - _pid_last_error) / delta
	_pid_last_error = error

	var control = pid_kp * error + pid_ki * _pid_error_sum + pid_kd * derivative
	control = clamp(control, -rotation_speed, rotation_speed)  # Limit control to rotation speed

	# 3. Apply steering (rotation rate limited by control)
	rotation += control * delta

	# 4. Move forward in the new heading
	position += Vector2.RIGHT.rotated(rotation) * speed * delta

func _on_body_entered(body: Node2D) -> void:
	body.take_damage(damage)
	queue_free()
