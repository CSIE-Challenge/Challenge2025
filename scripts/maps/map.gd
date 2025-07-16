class_name Map
extends Control

enum CellTerrain {
	OUT_OF_BOUNDS,
	EMPTY = 1,
	ROAD = 2,
	OBSTACLE = 3,
}

var game: Game

@onready var terrain: TileMapLayer = $Terrain
@onready var opponent_path: Path2D = $OpponentPath
@onready var system_path: Path2D = $SystemPath
@onready var flying_opponent_path: Path2D = $FlyingOpponentPath
@onready var flying_system_path: Path2D = $FlyingSystemPath


func _ready():
	pass


func get_enemy_z_index(_enemy: Enemy) -> int:
	if (
		_enemy.path_follow.get_parent() == $FlyingOpponentPath
		or _enemy.path_follow.get_parent() == $FlyingSystemPath
	):
		return Util.FLYING_LAYER
	return Util.ENEMY_LAYER


func global_to_local(global_pos: Vector2) -> Vector2:
	return terrain.to_local(global_pos)


func local_to_global(local_pos: Vector2) -> Vector2:
	return terrain.to_global(local_pos)


func global_to_cell(global_pos: Vector2) -> Vector2i:
	return terrain.local_to_map(global_to_local(global_pos))


func cell_to_global(cell_pos: Vector2i) -> Vector2:
	return local_to_global(terrain.map_to_local(cell_pos))


func get_cell_terrain(cell_pos: Vector2i) -> CellTerrain:
	var tile_data = terrain.get_cell_tile_data(cell_pos)
	if tile_data == null:
		return CellTerrain.OUT_OF_BOUNDS
	return tile_data.get_custom_data("type")


func get_local_terrain(local_pos: Vector2) -> CellTerrain:
	return get_cell_terrain(terrain.local_to_map(local_pos))


# display terrain overlay on hotkey
func _unhandled_input(event: InputEvent) -> void:
	if (
		InputMap.event_is_action(event, "toggle_terrain_overlay")
		and event.is_pressed()
		and not event.is_echo()
	):
		terrain.visible = not terrain.visible
