class_name Fort
extends Tower

var target_direction: float
var _map: Map

@onready var tower_body = $Tower
@onready var sprite = $Tower/AnimatedSprite2D
@onready var enemy_detector = $AimRange/CollisionShape2D


func enable(_global_position: Vector2, map: Map) -> void:
	enabled = true
	global_position = _global_position
	_map = map
	target_direction = _get_fort_direction()
	sprite.flip_h = cos(target_direction) < 0
	reload_timer.start(reload_seconds)


func _ready():
	super()
	enemy_detector.shape.radius = 0.5 * aim_range


# take aim when enabled
func _flip_sprite() -> void:
	return


func _on_reload_timer_timeout() -> void:
	var origin: Vector2 = $Tower/Marker2D.global_position
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
