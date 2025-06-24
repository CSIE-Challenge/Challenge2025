extends Node2D

@export var tower_scene: PackedScene

var preview_tower

@onready var tilemap: TileMapLayer = $TileMapLayer
@onready var towers_node: Node2D = $Towers
@onready var attack_UI: Control = $Attack

func _ready():
	preview_tower = tower_scene.instantiate()
	preview_tower.is_preview = true
	add_child(preview_tower)


func _process(_delta):
	var mouse_pos = get_global_mouse_position()
	var cell = tilemap.local_to_map(tilemap.to_local(mouse_pos))
	var world_pos = tilemap.map_to_local(cell)
	preview_tower.global_position = tilemap.to_global(world_pos)
	preview_tower.visible = handle_visibility_of_preview_tower()

	var valid = can_place_tower(cell)
	set_tower_color(preview_tower, valid)


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

func handle_visibility_of_preview_tower():
	if attack_UI.panel.visible and attack_UI.panel.get_global_rect().has_point(get_global_mouse_position()):
		return false
	if attack_UI.open_button.visible and attack_UI.open_button.get_global_rect().has_point(get_global_mouse_position()):
		return false
	return true
