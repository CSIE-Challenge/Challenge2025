class_name TowerWithMultipleBullet
extends TowerWithSingleBullet

const DIVIATE_ANGLES = [
	0, PI / 6, -PI / 6, PI / 12, -PI / 12, 3 * PI / 12, -3 * PI / 12, PI / 3, -PI / 3
]

@export var expected_bullet_number: int = 3


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		return
	if not anime.is_playing():
		anime.play("default")
	var attack_scene = sprite.sprite_frames.get_frame_count(sprite.animation) - 1
	wait_for_animation_timer.timeout.connect(self._on_fire_bullet, CONNECT_ONE_SHOT)
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION * attack_scene)


func _on_fire_bullet() -> void:
	if not (target != null and is_instance_valid(target)):
		_refresh_target()
		if target == null:
			has_cooldowned = true
			return
	var origin: Vector2 = $Tower/Marker2D.global_position
	var direction: float = (target.global_position - origin).angle()

	for i in range(expected_bullet_number):
		var bullet := bullet_scene.instantiate()
		self.get_parent().add_child(bullet)
		bullet.init(origin, direction + DIVIATE_ANGLES[i], target, damage)
