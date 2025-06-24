extends "res://scripts/tower.gd"


func _ready() -> void:
	damage = 12
	rotation_speed = 120
	aim_range = 1200
	reload_speed = 45
	if is_preview:
		apply_preview_appearance()
	else:
		built = true
		enemy_detector.shape.radius = 0.5 * aim_range
		reload_timer.wait_time = 60.0 / reload_speed
		reload_timer.start()


func shoot() -> void:
	var bullet = bullet_scene.instantiate()
	bullet.damage = damage
	var spawn_pos
	if current_shoot_turret == 0:
		spawn_pos = $Turret/Middle
	bullet.rotation = turret.rotation
	bullet.position = spawn_pos.position.rotated(turret.rotation)
	self.add_child(bullet)
	current_shoot_turret ^= 1
