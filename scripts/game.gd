class_name Game
extends Control


signal money_updated(money: int)
signal damage_taken(damage: int)


enum EnemySource { SYSTEM, OPPONENT }


const tower_scene := preload("res://scenes/tower.tscn")
const tower_cost = 5
const enemy_scene := preload("res://scenes/enemy.tscn")


@onready var _map: Map = $Map

var _money: int = 0:
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


func _place_tower(cell_pos: Vector2i, tower: Tower) -> void:
	if not _is_buildable(cell_pos):
		return
	var global_pos = _map.cell_to_global(cell_pos)

	tower.init(global_pos, $SignalBus)
	$TowerContainer.add_child(tower)

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

#endregion


#region Income

func _on_constant_income_timer_timeout() -> void:
	_money += _income_per_second

#endregion


#region Enemies

func _on_enemy_killed(enemy: Enemy) -> void:
	print("enemy killed: ", enemy)
	enemy.queue_free()


func _on_enemy_reached(enemy: Enemy) -> void:
	print("enemy reached: ", enemy)
	damage_taken.emit(enemy.damage)
	enemy.queue_free()


func summon_enemy(enemy: Enemy) -> void:
	var path: Path2D
	match enemy.source:
		EnemySource.SYSTEM:
			path = _map.system_path
		EnemySource.OPPONENT:
			path = _map.opponent_path
	enemy.killed.connect(self._on_enemy_killed.bind(enemy))
	enemy.reached.connect(self._on_enemy_reached.bind(enemy))
	path.add_child(enemy.path_follow)

#endregion


func _unhandled_input(event: InputEvent) -> void:
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
