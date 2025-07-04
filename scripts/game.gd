class_name Game
extends Control


signal money_updated(money: int)
signal damage_taken(damage: int)


enum EnemySource { SYSTEM, OPPONENT }


# todo: move tower parameters into the tower classes
const tower_scene := preload("res://scenes/tower.tscn")
const tower_cost = 5
const enemy_scene := preload("res://scenes/enemies/enemy.tscn")
const tower_ui_scene := preload("res://scenes/tower_ui.tscn")


@onready var _map: Map = $Map

var _money: int = 100:
	get:
		return _money
	set(value):
		money_updated.emit(value)
		_money = value
var _income_per_second = 10
var _built_towers: Dictionary = {}


#region Towers

func _is_buildable(cell_pos: Vector2i) -> bool:
	if _built_towers.has(cell_pos):
		return false
	if _money < tower_cost:
		return false
	return _map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _on_tower_upgraded(tower: Tower):
	var levelup_cost: int = tower.level * 10
	if _money >= levelup_cost:
		_money -= levelup_cost
		tower.upgrade()


func _on_tower_sold(tower: Tower, tower_ui: TowerUi):
	var refund := tower.level * 10
	_money += refund
	tower.queue_free()
	tower_ui.queue_free()
	var cell_pos = _map.global_to_cell(tower.global_position)
	_built_towers.erase(cell_pos)


func _place_tower(cell_pos: Vector2i, tower: Tower) -> void:
	if not _is_buildable(cell_pos):
		return
	var global_pos = _map.cell_to_global(cell_pos)

	self.add_child(tower)
	tower.init(global_pos)

	_money -= tower_cost
	_built_towers[cell_pos] = tower


func buy_tower(tower: Tower):
	var preview_color_callback = func(cell_pos: Vector2i) -> Previewer.PreviewMode:
		if _is_buildable(cell_pos):
			return Previewer.PreviewMode.SUCCESS
		return Previewer.PreviewMode.FAIL

	var previewer = Previewer.new(tower, preview_color_callback, _map, true)
	previewer.selected.connect(self._place_tower.bind(tower))
	self.add_child(previewer)


func _select_tower(tower: Tower):
	var tower_ui: TowerUi = tower_ui_scene.instantiate()
	self.add_child(tower_ui)
	tower_ui.global_position = tower.global_position
	tower_ui.upgraded.connect(self._on_tower_upgraded.bind(tower))
	tower_ui.sold.connect(self._on_tower_sold.bind(tower, tower_ui))


func _handle_tower_selection(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed):
		return
	var clicked_cell = _map.global_to_cell(get_global_mouse_position())
	if _built_towers.has(clicked_cell):
		_select_tower(_built_towers[clicked_cell])
		get_viewport().set_input_as_handled()

#endregion


#region Income

func _on_constant_income_timer_timeout() -> void:
	_money += _income_per_second

#endregion


#region Enemies

func summon_enemy(enemy: Enemy) -> void:
	enemy.game = self
	var path: Path2D
	match enemy.source:
		EnemySource.SYSTEM:
			path = _map.system_path
		EnemySource.OPPONENT:
			path = _map.opponent_path
	path.add_child(enemy.path_follow)

#endregion


func _unhandled_input(event: InputEvent) -> void:
	_handle_tower_selection(event)

	if (
			event is InputEventKey
			and event.pressed
			and (event.keycode == KEY_T)
	):
		buy_tower(tower_scene.instantiate())
		get_viewport().set_input_as_handled()
	if (
			event is InputEventKey
			and event.pressed
			and (event.keycode == KEY_E or event.keycode == KEY_S)
	):
		var source
		if event.keycode == KEY_E:
			source = EnemySource.OPPONENT
		else:
			source = EnemySource.SYSTEM
		var enemy := enemy_scene.instantiate()
		enemy.init(source)
		summon_enemy(enemy)
		get_viewport().set_input_as_handled()
