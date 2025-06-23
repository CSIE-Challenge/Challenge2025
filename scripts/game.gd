extends Node2D

@export var tower_scene: PackedScene

var preview_tower
var money: int = 0
var money_per_second: int = 1
const TOWER_COST = 5
var _money_timer := 0.0

@onready var tilemap: TileMapLayer = $TileMapLayer
@onready var towers_node: Node2D = $Towers


func _ready():
	preview_tower = tower_scene.instantiate()
	preview_tower.is_preview = true
	add_child(preview_tower)


func _process(_delta):
	var mouse_pos = get_global_mouse_position()
	var cell = tilemap.local_to_map(tilemap.to_local(mouse_pos))
	var world_pos = tilemap.map_to_local(cell)
	preview_tower.global_position = tilemap.to_global(world_pos)

	var valid = can_place_tower(cell)
	set_tower_color(preview_tower, valid)
	_money_timer += _delta
	if _money_timer > 1.0 :
		money += money_per_second
		_money_timer = 0.0




func set_tower_color(tower: Node2D, is_valid: bool):
	var color = Color(0, 1, 0, 0.5) if is_valid else Color(1, 0, 0, 0.5)
	for child in tower.get_children():
		if child is CanvasItem:
			child.modulate = color


func _unhandled_input(event: InputEvent):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var cell = tilemap.local_to_map(tilemap.to_local(get_global_mouse_position()))
		if can_place_tower(cell):
			place_tower(cell)


func can_place_tower(cell: Vector2i) -> bool:
	var tile_data = tilemap.get_cell_tile_data(cell)
	if tile_data == null:
		return false
	return tile_data.get_custom_data("buildable") == true


func place_tower(cell: Vector2i):
	var tower = tower_scene.instantiate()
	var world_pos = tilemap.map_to_local(cell)
	tower.global_position = tilemap.to_global(world_pos)
	towers_node.add_child(tower)
