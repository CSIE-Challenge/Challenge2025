class_name Map
extends Control

enum CellTerrain {
	OUT_OF_BOUNDS,
	EMPTY = 1,
	ROAD = 2,
	OBSTACLE = 3,
}

@onready var terrain: TileMapLayer = $Terrain
@onready var opponent_path: Path2D = $OpponentPath
@onready var system_path: Path2D = $SystemPath
# @onready var flying...


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
