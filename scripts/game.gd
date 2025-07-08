class_name Game
extends Control

signal damage_taken(damage: int)
signal buy_tower(tower_scene: PackedScene)
signal summon_enemy(unit_data: Dictionary)
signal buy_spell(spell_data)

# TODO: add flying path for system and opponent to map
enum EnemySource { SYSTEM, OPPONENT }

# todo: move tower parameters into the tower classes
const TOWER_SCENE := preload("res://scenes/towers/shy_guy_2a.tscn")
const ENEMY_SCENE := preload("res://scenes/enemies/enemy.tscn")
const TOWER_UI_SCENE := preload("res://scenes/tower_ui.tscn")

@export var spawner: Spawner
@export var status_panel: TextureRect

var score: int = 0
var money: int = 100
var income_per_second = 10
var kill_cnt = 0
var income_rate: float = 1
var built_towers: Dictionary = {}
var previewer: Previewer = null
var player_selection: IndividualPlayerSelection = null
var spell_dict: Dictionary
var op_game: Game
var _enemy_scene_cache = {}

@onready var _map: Map = $Map


func set_controller(_player_selection: IndividualPlayerSelection) -> void:
	player_selection = _player_selection
	player_selection.get_parent().remove_child(player_selection)
	status_panel.link_player_selection(player_selection)


func _ready() -> void:
	buy_tower.connect(_on_buy_tower)
	spawner.spawn_enemy.connect(_on_enemy_spawn)
	summon_enemy.connect(_on_enemy_summon)
    
	buy_spell.connect(_on_buy_spell)


func spend(cost: int) -> bool:
	if money >= cost:
		money -= cost
		return true
	return false


#region Towers


func _is_buildable(tower: Tower, cell_pos: Vector2i) -> bool:
	if built_towers.has(cell_pos):
		# TODO: Should replace current tower
		return false
	if money < tower.building_cost:
		return false
	return _map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _on_tower_sold(tower: Tower, tower_ui: TowerUi):
	var refund := tower.upgrade_cost
	money += refund
	tower.queue_free()
	tower_ui.queue_free()
	var cell_pos = _map.global_to_cell(tower.global_position)
	built_towers.erase(cell_pos)


func _place_tower(cell_pos: Vector2i, tower: Tower, map: Map) -> void:
	if not _is_buildable(tower, cell_pos):
		return
	var global_pos = _map.cell_to_global(cell_pos)

	self.add_child(tower)
	tower.enable(global_pos, map)

	money -= tower.building_cost
	built_towers[cell_pos] = tower


func _on_buy_tower(tower_scene: PackedScene):
	var tower = tower_scene.instantiate() as Tower
	var preview_color_callback = func(_tower: Tower, cell_pos: Vector2i) -> Previewer.PreviewMode:
		if money >= _tower.building_cost and _is_buildable(_tower, cell_pos):
			return Previewer.PreviewMode.SUCCESS
		return Previewer.PreviewMode.FAIL

	var previewer = Previewer.new(tower, preview_color_callback, _map, true)
	previewer.selected.connect(self._place_tower.bind(tower, _map))
	self.add_child(previewer)


func _select_tower(tower: Tower):
	var tower_ui: TowerUi = TOWER_UI_SCENE.instantiate()
	self.add_child(tower_ui)
	tower_ui.global_position = tower.global_position
	tower_ui.sold.connect(self._on_tower_sold.bind(tower, tower_ui))


func _handle_tower_selection(event: InputEvent) -> void:
	if not (
		event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed
	):
		return
	var clicked_cell = _map.global_to_cell(get_global_mouse_position())
	if built_towers.has(clicked_cell):
		_select_tower(built_towers[clicked_cell])
		get_viewport().set_input_as_handled()


#endregion

#region Income


func _on_constant_income_timer_timeout() -> void:
	money += income_rate * income_per_second


#endregion

#region Enemies


func _initialize_enemy_from_data(unit_data: Dictionary) -> Enemy:
	var scene_path = unit_data.get("scene_path")
	if scene_path == null or !ResourceLoader.exists(scene_path):
		print("Attempted to initialize Invalid Enemy Scene (%s)" % scene_path)
		return
	if !_enemy_scene_cache.has(scene_path):
		_enemy_scene_cache[scene_path] = load(scene_path)

	var enemy: Enemy = _enemy_scene_cache[scene_path].instantiate()
	var stats: Dictionary = unit_data.get("stats", {})
	enemy.max_health = stats.max_health
	enemy.max_speed = stats.max_speed
	enemy.damage = stats.damage
	enemy.flying = stats.flying
	return enemy


func _on_enemy_spawn(unit_data: Dictionary) -> void:
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.SYSTEM)


func _on_enemy_summon(unit_data: Dictionary) -> void:
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.OPPONENT)


func on_damage_dealt(damage: int) -> void:
	score += damage


func _deploy_enemy(enemy: Enemy, source: EnemySource) -> void:
	enemy.game = self
	enemy.init(source)
	var path: Path2D
	match source:
		EnemySource.SYSTEM:
			path = _map.system_path
		EnemySource.OPPONENT:
			path = _map.opponent_path
	path.add_child(enemy.path_follow)


#endregion

#region Spells


func _on_buy_spell(spell) -> void:
	if not spell.metadata.stats.target:
		var spell_node = $SpellManager.get_node(spell.metadata.name)
		spell_node.cast_spell()
	else:
		var original_spell_node = $SpellManager.get_node(spell.metadata.name)
		var spell_scene = load(spell.metadata.scene_path)
		var preview_spell_node = spell_scene.instantiate()
		var preview_color_callback = func(node, cell_pos: Vector2i) -> Previewer.PreviewMode:
			if money >= node.metadata.stats.cost and not node.is_on_cooldown:
				return Previewer.PreviewMode.SUCCESS
			return Previewer.PreviewMode.FAIL

		if previewer != null:
			previewer.free()

		previewer = Previewer.new(preview_spell_node, preview_color_callback, _map, true)
		previewer.selected.connect(self._place_spell.bind(original_spell_node))
		self.add_child(previewer)
		preview_spell_node.range_indicator.show()


func _place_spell(cell_pos: Vector2i, spell_node) -> void:
	var global_pos: Vector2 = _map.cell_to_global(cell_pos)
	spell_node.cast_spell(global_pos)


#endregion


func _process(_delta) -> void:
	status_panel.find_child("Money").text = "%d" % money
	status_panel.find_child("Income").text = "+%d" % income_per_second


func _unhandled_input(event: InputEvent) -> void:
	if (
		event is InputEventMouseButton
		and event.button_index == MOUSE_BUTTON_RIGHT
		and event.pressed
		and previewer != null
	):
		previewer.free()
	_handle_tower_selection(event)
