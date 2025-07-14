class_name TowerWithSingleBullet
extends Tower

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var marker = $Tower/Marker2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		return
	if not anime.is_playing():
		anime.play("default")
	var attack_scene = sprite.sprite_frames.get_frame_count(sprite.animation) - 1
	wait_for_animation_timer.timeout.connect(self._on_fire_bullet, CONNECT_ONE_SHOT)
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION * attack_scene)


func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		sprite.flip_h = cos(desired_angle) < 0
		if sprite.flip_h:
			marker.position.x = -abs(marker.position.x)
		else:
			marker.position.x = abs(marker.position.x)
