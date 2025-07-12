class_name TowerWithMultipleBullet
extends Tower

const SHOOTING_DURATION = 0.4

@export var expected_bullet_number: int = 3
@export var scattering_angle: float = PI / 6

var shooting_timer: Timer

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var marker = $Tower/Marker2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range
	shooting_timer = Timer.new()
	self.add_child(shooting_timer)
	#print(sprite.sprite_frames.get_frame_count(sprite.animation))


func _flip_sprite() -> void:
	if target != null:
		var desired_angle = (target.global_position - tower_body.global_position).angle()
		sprite.flip_h = cos(desired_angle) < 0
		if sprite.flip_h:
			marker.position.x = -abs(marker.position.x)
		else:
			marker.position.x = abs(marker.position.x)


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
	var bullet_to_shoot: int = roundi(randfn(expected_bullet_number, 3) + 0.5)
	_spawn_bullet(bullet_to_shoot, SHOOTING_DURATION / bullet_to_shoot)


func _spawn_bullet(bullet_left: int, shooting_interval: float) -> void:
	_refresh_target()
	if target == null:
		return
	var origin: Vector2 = $Tower/Marker2D.global_position
	var direction: float = (
		(target.global_position - origin).angle() + randfn(0.0, scattering_angle / 2)
	)
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target, damage)
	if bullet_left > 1:
		shooting_timer.timeout.connect(
			self._spawn_bullet.bind(bullet_left - 1, shooting_interval), CONNECT_ONE_SHOT
		)
		shooting_timer.start(shooting_interval)


func to_dict(coord: Vector2i) -> Dictionary:
	var dict: Dictionary = super(coord)
	dict["bullet_number"] = expected_bullet_number
	return dict
