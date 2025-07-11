class_name TowerWithMultipleBullet
extends Tower

@export var expected_bullet_number: int = 5
@export var scattering_angle: float = PI / 6

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		sprite.flip_h = cos(desired_angle) < 0


func _on_reload_timer_timeout() -> void:
	_refresh_target()
	if target == null:
		anime.stop()
		return
	if not anime.is_playing():
		anime.play("default")
	for i in range(roundi(randfn(expected_bullet_number, 3) + 0.5)):
		var origin: Vector2 = $Tower/Marker2D.global_position
		var direction: float = (
			(target.global_position - origin).angle() + randfn(0.0, scattering_angle / 6)
		)
		var bullet := bullet_scene.instantiate()
		self.get_parent().add_child(bullet)
		bullet.init(origin, direction, target)
