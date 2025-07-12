class_name Game
extends Control

signal damage_taken(damage: int)
signal buy_tower(tower_scene: PackedScene)
signal summon_enemy(unit_data: Dictionary)
signal buy_spell(spell_data)

enum EnemySource { SYSTEM, OPPONENT }

const TOWER_UI_SCENE := preload("res://scenes/tower_ui.tscn")
const DEPRECIATION_RATE := 0.9
const INTEREST_RATE := 1.02

@export var spawner: Spawner
@export var status_panel: TextureRect

# Various statistics
var score := 0
var kill_count := 0
var money_earned := 0
var tower_built := 0
var enemy_sent := 0
var api_called := 0

var money: int = 100
var income_per_second = 10
var player_selection: IndividualPlayerSelection = null
var income_rate: int = 1
var built_towers: Dictionary = {}
var previewer: Previewer = null
var spell_dict: Dictionary
var op_game: Game
var enemy_cooldown: Dictionary[int, SceneTreeTimer] = {}
var map: Map = null
var _enemy_scene_cache = {}


func set_controller(_player_selection: IndividualPlayerSelection) -> void:
	player_selection = _player_selection
	player_selection.get_parent().remove_child(player_selection)
	status_panel.link_player_selection(player_selection)


func set_map(map_scene: PackedScene):
	map = map_scene.instantiate()
	add_child(map)
	map.game = self


func _ready() -> void:
	buy_tower.connect(_on_buy_tower)
	spawner.spawn_enemy.connect(_on_enemy_spawn)
	summon_enemy.connect(_on_enemy_summon)

	buy_spell.connect(_on_buy_spell)


func spend(cost: int, income_impact: int = 0) -> bool:
	if money >= cost:
		money -= cost
		income_per_second = max(income_per_second + income_impact, 0)
		return true
	return false


#region Towers


func _is_buildable(tower: Tower, cell_pos: Vector2i) -> bool:
	if built_towers.has(cell_pos):
		var previous_tower = built_towers[cell_pos]
		if (
			(
				previous_tower.type == tower.type
				and (
					previous_tower.level_a > tower.level_a or previous_tower.level_b > tower.level_b
				)
			)
			or money + previous_tower.building_cost < tower.building_cost
		):
			return false
		if (
			previous_tower.type != tower.type
			and money + (previous_tower.building_cost * DEPRECIATION_RATE) < tower.building_cost
		):
			return false
	if money < tower.building_cost:
		return false
	return map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _on_tower_sold(tower: Tower, tower_ui: TowerUi, depreciation: bool):
	money += (
		(tower.building_cost * DEPRECIATION_RATE) as int if depreciation else tower.building_cost
	)
	tower.queue_free()
	if is_instance_valid(tower_ui):
		tower_ui.queue_free()
	var cell_pos = map.global_to_cell(tower.global_position)
	built_towers.erase(cell_pos)


func place_tower(cell_pos: Vector2i, tower: Tower) -> void:
	if not _is_buildable(tower, cell_pos):
		return

	if built_towers.has(cell_pos):
		var previous_tower = built_towers[cell_pos]
		var depreciation = (
			previous_tower.type != tower.type
			or previous_tower.level_a > tower.level_a
			or previous_tower.level_b > tower.level_b
		)
		_on_tower_sold(previous_tower, null, depreciation)

	var global_pos = map.cell_to_global(cell_pos)
	built_towers[cell_pos] = tower
	self.add_child(tower)
	tower.enable(global_pos, map)
	tower_built += 1

	money -= tower.building_cost
	built_towers[cell_pos] = tower


func _on_buy_tower(tower_scene: PackedScene):
	var tower = tower_scene.instantiate() as Tower
	var preview_color_callback = func(_tower: Tower, cell_pos: Vector2i) -> Previewer.PreviewMode:
		if _is_buildable(_tower, cell_pos):
			return Previewer.PreviewMode.SUCCESS
		return Previewer.PreviewMode.FAIL

	if previewer != null:
		self.remove_child(previewer)
		previewer.free()
	previewer = Previewer.new(tower, preview_color_callback, map, true)
	previewer.selected.connect(self.place_tower.bind(tower))
	self.add_child(previewer)


func _select_tower(tower: Tower):
	var tower_ui: TowerUi = TOWER_UI_SCENE.instantiate()
	self.add_child(tower_ui)
	tower_ui.global_position = tower.global_position
	tower_ui.sold.connect(self._on_tower_sold.bind(tower, tower_ui, true))


func _handle_tower_selection(event: InputEvent) -> void:
	if not (
		event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed
	):
		return
	var clicked_cell = map.global_to_cell(get_global_mouse_position())
	if built_towers.has(clicked_cell):
		_select_tower(built_towers[clicked_cell])
		get_viewport().set_input_as_handled()


#endregion

#region Income


func _on_constant_income_timer_timeout() -> void:
	var next_money = (money + income_rate * income_per_second) as int
	money_earned += next_money - money
	money = next_money


func _on_interest_timer_timeout() -> void:
	var next_money = (money * INTEREST_RATE) as int
	money_earned += next_money - money
	money = next_money


func on_subsidization(subsidy) -> void:
	if score < op_game.score:
		var next_money = money + subsidy
		money_earned += next_money - money
		money = next_money


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
	enemy.type = stats.type
	enemy.income_impact = stats.income_impact
	enemy.max_health = stats.max_health
	enemy.max_speed = stats.max_speed
	enemy.damage = stats.damage
	enemy.flying = stats.flying
	enemy.knockback_resist = stats.knockback_resist
	enemy.kill_reward = stats.kill_reward
	if enemy.flying:
		enemy.collision_layer = 4
		enemy.collision_mask = 8
	else:
		enemy.collision_layer = 1
		enemy.collision_mask = 2
	return enemy


func _on_enemy_spawn(unit_data: Dictionary) -> void:
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.SYSTEM)


func _on_enemy_summon(unit_data: Dictionary) -> void:
	op_game.enemy_sent += 1
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.OPPONENT)


func on_damage_dealt(damage: int) -> void:
	score += damage


func _deploy_enemy(enemy: Enemy, source: EnemySource) -> void:
	enemy.game = self
	enemy.init(source)
	var path: Path2D
	match source:
		EnemySource.SYSTEM:
			path = map.flying_system_path if enemy.flying else map.system_path
		EnemySource.OPPONENT:
			enemy_cooldown[enemy.type] = get_tree().create_timer(enemy.summon_cooldown)
			enemy_cooldown[enemy.type].timeout.connect(_enemy_cooldown_ended.bind(enemy.type))
			path = map.flying_opponent_path if enemy.flying else map.opponent_path
	path.add_child(enemy.path_follow)


func get_all_enemies() -> Array:
	var list: Array = []
	for path in map.system_path.get_children():
		list.push_back(path.get_children()[0])
	for path in map.opponent_path.get_children():
		list.push_back(path.get_children()[0])
	return list


func _enemy_cooldown_ended(enemy_type: Enemy.EnemyType):
	enemy_cooldown.erase(enemy_type)


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
		var preview_color_callback = func(node, _cell_pos: Vector2i) -> Previewer.PreviewMode:
			if money >= node.metadata.stats.cost and not node.is_on_cooldown:
				return Previewer.PreviewMode.SUCCESS
			return Previewer.PreviewMode.FAIL

		if previewer != null:
			previewer.free()

		previewer = Previewer.new(preview_spell_node, preview_color_callback, map, true)
		previewer.selected.connect(self._place_spell.bind(original_spell_node))
		self.add_child(previewer)
		preview_spell_node.range_indicator.show()


func _place_spell(cell_pos: Vector2i, spell_node) -> void:
	var global_pos: Vector2 = map.cell_to_global(cell_pos)
	spell_node.cast_spell(global_pos)


#endregion


func _process(_delta) -> void:
	status_panel.find_child("Money").text = "%d" % money
	status_panel.find_child("Income").text = "+%d" % [income_per_second * income_rate]


func _unhandled_input(event: InputEvent) -> void:
	_handle_tower_selection(event)
