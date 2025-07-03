extends Control


const tower_scene := preload("res://scenes/tower.tscn")
const tower_cost = 5


@onready var _map: Map = $Map

var _money = 100
var _built_towers: Dictionary = {}


func _is_buildable(cell_pos: Vector2i) -> bool:
	if _built_towers.has(cell_pos):
		return false
	if _money < tower_cost:
		return false
	return _map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _place_tower(cell_pos: Vector2i) -> void:
	if not _is_buildable(cell_pos):
		return
	var global_pos = _map.cell_to_global(cell_pos)

	var tower = tower_scene.instantiate()
	tower.global_position = global_pos
	$TowerContainer.add_child(tower)

	_money -= tower_cost
	_built_towers[cell_pos] = tower


func _buy_tower():
	var preview_color_callback = func(cell_pos: Vector2i) -> Previewer.PreviewMode:
		if _is_buildable(cell_pos):
			return Previewer.PreviewMode.SUCCESS
		return Previewer.PreviewMode.FAIL

	var previewer = Previewer.new(tower_scene.instantiate(), preview_color_callback, _map, true)
	previewer.selected.connect(self._place_tower)
	self.add_child(previewer)


func _unhandled_input(event: InputEvent) -> void:
	if (
			event is InputEventKey
			and event.pressed
			and (event.keycode == KEY_T)
	):
		_buy_tower()
		get_viewport().set_input_as_handled()


func _process(_delta: float) -> void:
	return
