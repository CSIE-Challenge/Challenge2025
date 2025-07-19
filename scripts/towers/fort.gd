class_name Fort
extends Tower

enum Direction { LEFT, RIGHT, UPPER, LOWER }

var target_direction: float
var marker: Marker2D
var animation: StringName = "LeftRight"  # Default scene
var _map: Map


func enable(_global_position: Vector2, map: Map) -> void:
	global_position = _global_position
	_map = map
	var dir = _get_fort_direction()
	match dir:
		Direction.LOWER:
			marker = $Tower/UpperMarker
			animation = "Upper"
			target_direction = -PI / 2
		Direction.UPPER:
			marker = $Tower/LowerMarker
			animation = "Lower"
			target_direction = PI / 2
		Direction.RIGHT:
			marker = $Tower/LeftRightMarker
			animation = "LeftRight"
			marker.position.x = abs(marker.position.x)
			target_direction = 0
		Direction.LEFT:
			marker = $Tower/LeftRightMarker
			animation = "LeftRight"
			sprite.flip_h = true
			marker.position.x = -abs(marker.position.x)
			target_direction = -PI
	sprite.set_animation(animation)
	reload_timer.start(reload_seconds)


func _ready():
	super()
	sprite.set_animation(animation)  # Default scene


func _on_reload_timer_timeout() -> void:
	reload_timer.start(reload_seconds)
	if not anime.is_playing():
		anime.play(animation)
	var attack_scene = sprite.sprite_frames.get_frame_count(sprite.animation) - 2
	wait_for_animation_timer.start(ANIMATION_FRAME_DURATION * attack_scene)


func _on_fire_bullet() -> void:
	var origin: Vector2 = marker.global_position
	var direction: float = target_direction
	var bullet := bullet_scene.instantiate()
	self.get_parent().add_child(bullet)
	bullet.init(origin, direction, target, damage)


func _get_fort_direction() -> Direction:
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
			best_direction = dir
	match best_direction:
		[1, 0]:
			return Direction.RIGHT
		[-1, 0]:
			return Direction.LEFT
		[0, 1]:
			return Direction.UPPER
	return Direction.LOWER
