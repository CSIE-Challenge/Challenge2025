class_name Fort
extends Tower

var target_direction: float
var marker: Marker2D
var animation: StringName = "LeftRight"  # Default scene
var _map: Map

@onready var sprite = $Tower/AnimatedSprite2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func enable(_global_position: Vector2, map: Map) -> void:
	global_position = _global_position
	_map = map
	target_direction = _get_fort_direction()
	if sin(target_direction) < -0.5:
		marker = $Tower/UpperMarker
		animation = "Upper"
	elif sin(target_direction) > 0.5:
		marker = $Tower/LowerMarker
		animation = "Lower"
	else:
		marker = $Tower/LeftRightMarker
		animation = "LeftRight"
		sprite.flip_h = cos(target_direction) < 0
		if sprite.flip_h:
			marker.position.x = -abs(marker.position.x)
		else:
			marker.position.x = abs(marker.position.x)
	sprite.set_animation(animation)
	reload_timer.start(reload_seconds)


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range
	sprite.set_animation(animation)  # Default scene


func _on_reload_timer_timeout() -> void:
	if not anime.is_playing():
		anime.play(animation)
	var attack_scene = sprite.sprite_frames.get_frame_count(sprite.animation) - 1
	wait_for_animation_timer.timeout.connect(self._on_fire_bullet, CONNECT_ONE_SHOT)
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION * attack_scene)


func _on_fire_bullet() -> void:
	var origin: Vector2 = marker.global_position
	var direction: float = target_direction
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target, damage)


func _get_fort_direction() -> float:
	var direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
	var best_direction = PI
	var best_count = 0
	for dir in direction:
		var cur_x = _map.global_to_cell(self.global_position).x + dir[0]
		var cur_y = _map.global_to_cell(self.global_position).y + dir[1]
		var terrain_type = _map.get_cell_terrain(Vector2i(cur_x, cur_y))
		var count = 0
		while terrain_type != _map.CellTerrain.OUT_OF_BOUNDS:
			if terrain_type == _map.CellTerrain.ROAD:
				count += 1
			cur_x += dir[0]
			cur_y += dir[1]
			terrain_type = _map.get_cell_terrain(Vector2i(cur_x, cur_y))
		if count > best_count:
			best_count = count
			best_direction = PI * min(dir[0], 0) + PI / 2 * dir[1]
	return best_direction
