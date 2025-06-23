extends StaticBody2D

@export var bullet_scene: PackedScene

var damage: int = 2
var rotation_speed: float = 90.0  # degree per second
var aim_range: float = 450.0
var reload_speed: float = 240  # per minute
var level: int = 1
var current_shoot_turret: int = 0  # 0 for left, 1 for right

var enemies: Array = []

var built: bool = false
var is_preview := false

@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D
@onready var reload_timer = $ReloadTimer


func _ready():
	if is_preview:
		apply_preview_appearance()
	else:
		built = true
		enemy_detector.shape.radius = 0.5 * aim_range
		reload_timer.wait_time = 60.0 / reload_speed
		reload_timer.start()


func apply_preview_appearance():
	for child in get_children():
		if child is CanvasItem:
			child.modulate = Color(1, 1, 1, 0.5)
	set_process(false)


func _physics_process(delta: float) -> void:
	#print(enemies)
	if enemies.size() > 0 and built:
		aim(delta)


func aim(delta: float) -> void:
	var first_enemy = enemies[0]
	var pos_diff: Vector2 = self.position - first_enemy.position
	var angle: float = atan2(pos_diff.y, pos_diff.x)
	var angle_diff = angle - turret.rotation - PI / 2
	if angle_diff < -2 * PI:
		angle_diff += 2 * PI
	if angle_diff > 2 * PI:
		angle_diff -= 2 * PI
	#print(angle_diff)
	if (angle_diff < PI and angle_diff > 0) or (angle_diff < -PI and angle_diff > -2 * PI):
		turret.rotate(delta * deg_to_rad(rotation_speed))
	else:
		turret.rotate(-delta * deg_to_rad(rotation_speed))


func shoot() -> void:
	var bullet = bullet_scene.instantiate()
	bullet.damage = damage
	var spawn_pos
	if current_shoot_turret == 0:
		spawn_pos = $Turret/Left
	else:
		spawn_pos = $Turret/Right
	bullet.rotation = turret.rotation
	bullet.position = spawn_pos.position.rotated(turret.rotation)
	self.add_child(bullet)
	current_shoot_turret ^= 1


func _on_aim_range_body_entered(body: Node2D) -> void:
	if not body.is_in_group("enemy"):
		return
	enemies.append(body.get_parent())


func _on_aim_range_body_exited(body: Node2D) -> void:
	enemies.erase(body.get_parent())


func _on_reload_timer_timeout() -> void:
	if enemies.size() > 0:
		shoot()
