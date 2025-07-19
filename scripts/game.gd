class_name Game
extends Control

signal damage_taken(damage: int)
signal buy_tower(tower_scene: PackedScene)  # handler
signal place_tower(coordinate: Vector2i, tower: Tower)  # handler
signal demolish_tower(coordinate: Vector2i)  # handler
signal tower_placed(coordinate: Vector2i)  # singal
signal tower_demolished(coordinate: Vector2i)  # singal
signal summon_enemy(unit_data: Dictionary)
signal buy_spell(spell_data)
signal on_manual_control_changed(value: bool)

enum EnemySource { SYSTEM, OPPONENT }

const TOWER_UI_SCENE := preload("res://scenes/tower_ui.tscn")
const DEPRECIATION_RATE := 0.9
const INTEREST_RATE := 1.02
const WAVE_HP_INCREASE_RATE := 1.1
const WAVE_SPEED_INCREASE_RATE := 1.1
const YELLOW := Color("#e2dd77")
const RED := Color("#cf0404")
const BOO_DURATION := 2

@export var spawner: Spawner
@export var status_panel: TextureRect

# Various statistics
var score := 0
var display_score := 0
var kill_count := 0
var money_earned := 0
var tower_built := 0
var enemy_sent := 0
var api_called := 0
var api_succeed := 0
var chat_total_length := 0

var player_selection: IndividualPlayerSelection = null
var money: int = 300
var income_per_second = 50
var kill_reward_within_second = 0
var display_kill_reward = 0
var income_rate: int = 1
var shop_discount: float = 1.0
var chat_name_color: String = "ffffff"
var built_towers: Dictionary = {}
var previewer: Previewer = null
var spell_dict: Dictionary
var op_game: Game
var enemy_cooldown: Dictionary[int, Timer] = {}
var map: Map = null
var frozen := true
var during_boo := false
var boo_timer: Timer
var no_damage := false
var no_cooldown := false
var current_hp_multiplier: float = 1
var current_speed_multiplier: float = 1
var is_manually_controlled := false:  # only used in water map
	get:
		return is_manually_controlled
	set(value):
		is_manually_controlled = value
		self.on_manual_control_changed.emit(value)
var premium_api_quota: int = -1
var has_started := false

var _enemy_scene_cache = {}
@onready var danmaku_scene = preload("res://scenes/danmaku.tscn")

@onready var no_cooldown_timer = $NoCooldownTimer
@onready var no_damage_timer = $NoDamageTimer


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
	place_tower.connect(_on_place_tower)
	demolish_tower.connect(_on_demolish_tower)
	spawner.spawn_enemy.connect(_on_enemy_spawn)
	summon_enemy.connect(_on_enemy_summon)
	spawner.wave_end.connect(_on_wave_end)

	buy_spell.connect(_on_buy_spell)
	_process(0)

	boo_timer = Timer.new()
	self.add_child(boo_timer)
	boo_timer.one_shot = true
	boo_timer.timeout.connect(_on_boo_end)


func start() -> void:
	has_started = true
	process_mode = Node.PROCESS_MODE_PAUSABLE


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
					(
						previous_tower.level_a > tower.level_a
						or previous_tower.level_b > tower.level_b
					)
					or (
						previous_tower.level_a == tower.level_a
						and previous_tower.level_b == tower.level_b
					)
				)
			)
			or (
				money + previous_tower.building_cost * shop_discount
				< tower.building_cost * shop_discount
			)
		):
			return false
		if (
			previous_tower.type != tower.type
			and (
				money + (previous_tower.building_cost * shop_discount * DEPRECIATION_RATE)
				< tower.building_cost * shop_discount
			)
		):
			return false
	if money < tower.building_cost * shop_discount:
		return false
	return map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _on_tower_sold(tower: Tower, tower_ui: TowerUi, depreciation: bool):
	money += (
		(tower.building_cost * shop_discount * DEPRECIATION_RATE) as int
		if depreciation
		else int(tower.building_cost * shop_discount)
	)
	tower.queue_free()
	if is_instance_valid(tower_ui):
		tower_ui.queue_free()
	var cell_pos = map.global_to_cell(tower.global_position)
	built_towers.erase(cell_pos)
	tower_demolished.emit(cell_pos)


func _on_place_tower(cell_pos: Vector2i, tower: Tower) -> void:
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
	self.tower_placed.emit(cell_pos)

	money -= int(tower.building_cost * shop_discount)
	built_towers[cell_pos] = tower


func _on_demolish_tower(cell_pos: Vector2i) -> void:
	if built_towers.has(cell_pos):
		_on_tower_sold(built_towers[cell_pos], null, true)


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
	previewer.selected.connect(self._on_place_tower.bind(tower))
	self.add_child(previewer)


func _select_tower(tower: Tower, left: bool, up: bool):
	var tower_ui: TowerUi = TOWER_UI_SCENE.instantiate()
	tower.add_child(tower_ui)
	tower_ui.global_position = tower.global_position
	await get_tree().process_frame
	var ui_size = tower_ui.size
	if left:
		tower_ui.global_position.x -= ui_size.x
	if up:
		tower_ui.global_position.y -= ui_size.y
	tower_ui.sold.connect(self._on_tower_sold.bind(tower, tower_ui, true))


func _handle_tower_selection(event: InputEvent) -> void:
	if not (
		event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed
	):
		return
	var clicked_cell = map.global_to_cell(get_global_mouse_position())
	if built_towers.has(clicked_cell):
		_select_tower(built_towers[clicked_cell], clicked_cell.x > 13, clicked_cell.y > 16)
		get_viewport().set_input_as_handled()


#endregion

#region Income


func get_modified_income_per_second() -> int:
	return (income_rate * income_per_second) as int


func _on_constant_income_timer_timeout() -> void:
	var next_money = money + get_modified_income_per_second()
	money_earned += next_money - money
	money = next_money
	if not during_boo:
		display_kill_reward = kill_reward_within_second
	kill_reward_within_second = 0


func _on_interest_timer_timeout() -> void:
	var next_money = (money * INTEREST_RATE) as int
	money_earned += next_money - money
	money = next_money


func on_boo_called(value: int) -> void:
	during_boo = true
	op_game.during_boo = true
	# Not regarded as money_earned
	money += value
	op_game.money -= value
	display_kill_reward = value
	op_game.display_kill_reward = -value
	status_panel.find_child("KillReward").add_theme_color_override("font_color", RED)
	op_game.status_panel.find_child("KillReward").add_theme_color_override("font_color", RED)
	boo_timer.start(BOO_DURATION)
	AudioManager.boo.play()


func _on_boo_end() -> void:
	display_kill_reward = kill_reward_within_second
	op_game.display_kill_reward = op_game.kill_reward_within_second
	status_panel.find_child("KillReward").text = _get_signed_string_number(display_kill_reward)
	op_game.status_panel.find_child("KillReward").text = _get_signed_string_number(
		op_game.display_kill_reward
	)
	status_panel.find_child("KillReward").add_theme_color_override("font_color", YELLOW)
	op_game.status_panel.find_child("KillReward").add_theme_color_override("font_color", YELLOW)
	during_boo = false
	op_game.during_boo = false


#endregion

#region Enemies


func _on_wave_end() -> void:
	current_hp_multiplier *= WAVE_HP_INCREASE_RATE
	current_speed_multiplier *= WAVE_SPEED_INCREASE_RATE


func _initialize_enemy_from_data(unit_data: Dictionary) -> Enemy:
	var scene_path = unit_data.get("scene_path")
	if scene_path == null or !ResourceLoader.exists(scene_path):
		push_error("[Game] Attempted to initialize invalid enemy scene (%s)" % scene_path)
		return
	if !_enemy_scene_cache.has(scene_path):
		_enemy_scene_cache[scene_path] = load(scene_path)

	var enemy: Enemy = _enemy_scene_cache[scene_path].instantiate()
	var stats: Dictionary = unit_data.get("stats", {})
	enemy.type = stats.type
	enemy.income_impact = stats.income_impact
	enemy.max_health = stats.max_health * current_hp_multiplier
	enemy.max_speed = stats.max_speed * current_speed_multiplier
	enemy.damage = stats.damage
	enemy.flying = stats.flying
	enemy.knockback_resist = stats.knockback_resist
	enemy.kill_reward = stats.kill_reward
	enemy.summon_cooldown = stats.cooldown
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
	if not no_damage:
		score += damage


func take_damage(damage: int) -> void:
	emit_signal("damage_taken", damage)


func _deploy_enemy(enemy: Enemy, source: EnemySource) -> void:
	enemy.game = self
	enemy.init(source)
	var path: Path2D
	match source:
		EnemySource.SYSTEM:
			path = map.flying_system_path if enemy.flying else map.system_path
		EnemySource.OPPONENT:
			if not no_cooldown:
				var timer = Timer.new()
				enemy_cooldown[enemy.type] = timer
				timer.wait_time = enemy.summon_cooldown
				timer.one_shot = true
				add_child(timer)
				timer.timeout.connect(_enemy_cooldown_ended.bind(enemy.type))
				timer.start()
			path = map.flying_opponent_path if enemy.flying else map.opponent_path
	path.add_child(enemy.path_follow)


func get_all_enemies() -> Array:
	var list: Array = []
	for path in map.system_path.get_children():
		list.push_back(path.get_children()[0])
	for path in map.opponent_path.get_children():
		list.push_back(path.get_children()[0])
	for path in map.flying_system_path.get_children():
		list.push_back(path.get_children()[0])
	for path in map.flying_opponent_path.get_children():
		list.push_back(path.get_children()[0])
	return list


func _enemy_cooldown_ended(enemy_type: Enemy.EnemyType):
	enemy_cooldown[enemy_type].queue_free()
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
		var preview_color_callback = func(_node, _cell_pos: Vector2i) -> Previewer.PreviewMode:
			if not $SpellManager.get_node(spell.metadata.name).is_on_cooldown:
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


func freeze() -> void:
	frozen = true


func _get_signed_string_number(value: int) -> String:
	if value == 0:
		return ""
	return "+%d" % value if value > 0 else "%d" % value


func _process(_delta) -> void:
	if !frozen:
		display_score = score
	status_panel.find_child("Money").text = "%d" % money
	status_panel.find_child("Income").text = "+%d" % get_modified_income_per_second()
	if income_rate > 1:
		status_panel.find_child("Income").text += " ×%d" % income_rate
	status_panel.find_child("KillReward").text = _get_signed_string_number(display_kill_reward)
	status_panel.find_child("ApiQuota").text = "%d" % max(0, premium_api_quota)


func _unhandled_input(event: InputEvent) -> void:
	_handle_tower_selection(event)


func _turbo_off() -> void:
	no_cooldown = false


func _damage_off() -> void:
	no_damage = false


func send_danmaku(text: String, _size := 24, color := Color.WHITE):
	var danmaku: Label = danmaku_scene.instantiate()
	var danmaku_layer = get_node("../../danmaku_layer")
	danmaku.setup(text, _size, color)
	var y_position = randf_range(50, 800)
	danmaku.position = Vector2(get_viewport_rect().size.x, y_position)
	danmaku_layer.add_child(danmaku)
