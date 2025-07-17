class_name Agent
extends Node
enum GameStatus { PREPARING, RUNNING, PAUSED }
enum EnemyType {
	BUZZY_BEETLE,
	GOOMBA,
	KOOPA_JR,
	KOOPA_PARATROOPA,
	KOOPA,
	SPINY_SHELL,
	WIGGLER,
}
enum SpellType { POISON, DOUBLE_INCOME, TELEPORT }
enum StatusCode {
	OK = 200,
	ILLFORMED_COMMAND = 400,
	AUTH_FAIL = 401,
	ILLEGAL_ARGUMENT = 402,
	COMMAND_ERR = 403,
	NOT_FOUND = 404,
	TOO_FREQUENT = 405,
	NOT_STARTED = 406,
	PAUSED = 407,
	INTERNAL_ERR = 500,
	CLIENT_ERR = 501
}

const TOWER_SCENES = [
	[
		preload("res://scenes/towers/fire_mario_1.tscn"),
		preload("res://scenes/towers/fire_mario_2a.tscn"),
		preload("res://scenes/towers/fire_mario_2b.tscn"),
		preload("res://scenes/towers/fire_mario_3a.tscn"),
		preload("res://scenes/towers/fire_mario_3b.tscn")
	],
	[
		preload("res://scenes/towers/ice_luigi_1.tscn"),
		preload("res://scenes/towers/ice_luigi_2a.tscn"),
		preload("res://scenes/towers/ice_luigi_2b.tscn"),
		preload("res://scenes/towers/ice_luigi_3a.tscn"),
		preload("res://scenes/towers/ice_luigi_3b.tscn")
	],
	[
		preload("res://scenes/towers/donkey_kong_1.tscn"),
		preload("res://scenes/towers/donkey_kong_2a.tscn"),
		preload("res://scenes/towers/donkey_kong_2b.tscn"),
		preload("res://scenes/towers/donkey_kong_3a.tscn"),
		preload("res://scenes/towers/donkey_kong_3b.tscn")
	],
	[
		preload("res://scenes/towers/fort_1.tscn"),
		preload("res://scenes/towers/fort_2a.tscn"),
		preload("res://scenes/towers/fort_2b.tscn"),
		preload("res://scenes/towers/fort_3a.tscn"),
		preload("res://scenes/towers/fort_3b.tscn")
	],
	[
		preload("res://scenes/towers/shy_guy_1.tscn"),
		preload("res://scenes/towers/shy_guy_2a.tscn"),
		preload("res://scenes/towers/shy_guy_2b.tscn"),
		preload("res://scenes/towers/shy_guy_3a.tscn"),
		preload("res://scenes/towers/shy_guy_3b.tscn")
	]
]
const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")
const LEVEL_TO_INDEX: Dictionary = {"1": 0, "2a": 1, "2b": 2, "3a": 3, "3b": 4}

var pixelcat_cnt: int = 1
var player_id: int
var game_running: bool = false
var send_pixelcat: bool = false
var ongoing_round: Round = null
var game_self: Game = null
var game_other: Game = null
var chat_node: Node = null

var sys_paths: Array = [[], []]
var opp_paths: Array = [[], []]

var pixel_cat_str: String


func _ready() -> void:
	pixel_cat_str = Util.load_json("res://data/pixelcat.json")["data"]


func start_game(_round: Round, _game_self: Game, _game_other: Game) -> void:
	game_running = true
	ongoing_round = _round
	game_self = _game_self
	game_other = _game_other


#region General


func _get_game_status() -> Array:
	if not game_running:
		return [StatusCode.OK, GameStatus.PREPARING]
	if get_tree().paused:
		return [StatusCode.OK, GameStatus.PAUSED]
	return [StatusCode.OK, GameStatus.RUNNING]


#endregion

#region MapInfo


func _get_all_terrain() -> Array:
	var map = game_self.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find map"]

	# Get the terrain without knowing the map size
	var all_terrain: Array[Array] = []
	var row: int = 0
	var col: int = 0
	while map.get_cell_terrain(Vector2i(row, col)) != map.CellTerrain.OUT_OF_BOUNDS:
		var line: Array = []
		while map.get_cell_terrain(Vector2i(row, col)) != map.CellTerrain.OUT_OF_BOUNDS:
			line.push_back(map.get_cell_terrain(Vector2i(row, col)))
			col += 1
		all_terrain.push_back(line)
		row += 1
		col = 0
	return [StatusCode.OK, all_terrain]


func _get_terrain(_coord: Vector2i) -> Array:
	var map = game_self.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find map"]

	return [StatusCode.OK, map.get_cell_terrain(_coord)]


func _get_scores(_owned: bool) -> Array:
	var result: int
	if _owned == true:
		result = game_self.score
	else:
		result = game_other.display_score
	return [StatusCode.OK, result]


func _get_current_wave() -> Array:
	var wave = ongoing_round.get_node("Spawner")
	if not wave:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find wave"]
	var wave_num: int = wave.current_wave_data.wave_number
	return [StatusCode.OK, wave_num]


func _get_remain_time() -> Array:
	if not game_running:
		return [StatusCode.OK, 1]
	var time_left = ongoing_round.get_node("GameTimer").time_left
	if time_left == null:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find timeleft"]
	return [StatusCode.OK, time_left]


func _get_time_until_next_wave() -> Array:
	var time_left = ongoing_round.get_node("Spawner").next_wave_timer.time_left
	if time_left == null:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find timeleft till next wave"]
	return [StatusCode.OK, time_left]


func _get_money(_owned: bool) -> Array:
	var result: int
	if _owned == true:
		result = int(game_self.status_panel.find_child("Money").text)
	else:
		result = int(game_other.status_panel.find_child("Money").text)
	return [StatusCode.OK, result]


func _get_income(_owned: bool) -> Array:
	var income: int
	if _owned == true:
		income = int(game_self.status_panel.find_child("Income").text)
	else:
		income = int(game_other.status_panel.find_child("Income").text)
	return [StatusCode.OK, income]


func _get_system_path(_fly: bool) -> Array:
	var map: Map = game_self.map
	if not map:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find map"]

	var index = int(_fly)
	if not sys_paths[index].is_empty():
		return [StatusCode.OK, sys_paths[index]]

	var curve: Curve2D
	if _fly:
		curve = map.flying_system_path.curve
	else:
		curve = map.system_path.curve
	var length := curve.get_baked_length()
	var interval := 2.0
	var t := 0.0

	while t < length:
		var pos: Vector2 = curve.sample_baked(t)
		var cell: Vector2i = map.global_to_cell(map.local_to_global(pos))
		if 1 <= cell[0] and cell[0] <= 14 and 1 <= cell[1] and cell[1] <= 19:
			if cell not in sys_paths[index]:
				sys_paths[index].append(cell)
		t += interval

	var end_pos: Vector2 = curve.sample_baked(length)
	var end_cell: Vector2i = map.global_to_cell(map.local_to_global(end_pos))
	if end_cell not in sys_paths[index]:
		sys_paths[index].append(end_cell)
	return [StatusCode.OK, sys_paths[index]]


func _get_opponent_path(_fly: bool) -> Array:
	var map: Map = game_self.map
	if not map:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find map"]

	var index = int(_fly)
	if not opp_paths[index].is_empty():
		return [StatusCode.OK, opp_paths[index]]

	var curve: Curve2D
	if _fly:
		curve = map.flying_opponent_path.curve
	else:
		curve = map.opponent_path.curve
	var length := curve.get_baked_length()
	var interval := 2.0
	var t := 0.0

	while t < length:
		var pos: Vector2 = curve.sample_baked(t)
		var cell: Vector2i = map.global_to_cell(map.local_to_global(pos))
		if 1 <= cell[0] and cell[0] <= 14 and 1 <= cell[1] and cell[1] <= 19:
			if cell not in opp_paths[index]:
				opp_paths[index].append(cell)
		t += interval

	var end_pos: Vector2 = curve.sample_baked(length)
	var end_cell: Vector2i = map.global_to_cell(map.local_to_global(end_pos))
	if end_cell not in opp_paths[index]:
		opp_paths[index].append(end_cell)
	return [StatusCode.OK, opp_paths[index]]


#endregion

#region Tower


#gdlint: disable=max-returns
func _place_tower(_type: Tower.TowerType, _level: String, _coord: Vector2i) -> Array:
	var map = game_self.get_node("Map")

	if not map:
		return [StatusCode.INTERNAL_ERR, "Error: cannot find map"]

	if map.get_cell_terrain(_coord) != Map.CellTerrain.EMPTY:
		return [StatusCode.COMMAND_ERR, "Error: invalid coordinate for building tower"]

	if (not _type in range(0, 6)) or (not _level in LEVEL_TO_INDEX.keys()):
		return [StatusCode.ILLEGAL_ARGUMENT, "Error: 'type' out of range or 'level' invalid"]

	var tower = TOWER_SCENES[_type - 1][LEVEL_TO_INDEX[_level]].instantiate()
	if game_self.built_towers.has(_coord):
		var previous_tower = game_self.built_towers[_coord]
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
			or game_self.money + previous_tower.building_cost < tower.building_cost
		):
			tower.free()
			return [StatusCode.COMMAND_ERR, "Error: can't upgrade tower"]
		if (
			previous_tower.type != tower.type
			and (
				game_self.money + (previous_tower.building_cost * game_self.DEPRECIATION_RATE)
				< tower.building_cost
			)
		):
			tower.free()
			return [StatusCode.COMMAND_ERR, "Error: not enough money"]

	if game_self.money < tower.building_cost:
		tower.free()
		return [StatusCode.COMMAND_ERR, "Error: not enough money"]
	game_self.place_tower.emit(_coord, tower)
	return [StatusCode.OK]


func _get_all_towers(_owned: bool) -> Array:
	var towers: Array = []
	if _owned:
		for key in game_self.built_towers.keys():
			var tower_dict = game_self.built_towers[key].to_dict(key)
			towers.append(tower_dict)
		return [StatusCode.OK, towers]
	for key in game_other.built_towers.keys():
		var tower_dict = game_other.built_towers[key].to_dict(key)
		towers.append(tower_dict)
	return [StatusCode.OK, towers]


func _get_tower(_owned: bool, _coord: Vector2i) -> Array:
	var towers_dict: Dictionary
	if _owned:
		towers_dict = game_self.built_towers
	else:
		towers_dict = game_other.built_towers
	if towers_dict.has(_coord):
		var dict = towers_dict[_coord].to_dict(_coord)
		return [StatusCode.OK, dict]
	return [StatusCode.OK, {}]


func _sell_tower(_coord: Vector2i) -> Array:
	if not game_self.built_towers.has(_coord):
		return [StatusCode.COMMAND_ERR, "No built tower on designated coordinate"]
	var tower: Tower = game_self.built_towers[_coord]
	game_self._on_tower_sold(tower, null, true)
	return [StatusCode.OK]


func _set_strategy(_coord: Vector2i, new_strategy: Tower.TargetStrategy) -> Array:
	if (not game_self.built_towers.has(_coord)) or (not new_strategy in range(3)):
		return [
			StatusCode.ILLEGAL_ARGUMENT, "No built tower on 'coord' or incorrect 'new_strategy'"
		]
	var tower: Tower = game_self.built_towers[_coord]
	tower.set_strategy(new_strategy)
	return [StatusCode.OK]


#endregion

#region Enemy


func _get_unit_dict(_type: EnemyType) -> Dictionary:
	var enemy_name: Array = [
		"buzzy_beetle", "goomba", "koopa_jr", "koopa_paratroopa", "koopa", "spiny_shell", "wiggler"
	]
	var unit_data = EnemyData.new()
	var data = unit_data.unit_data_list[enemy_name[_type]]
	return data


func _spawn_unit(_type: EnemyType) -> Array:
	var data = _get_unit_dict(_type)
	if game_other.enemy_cooldown.has(_type):
		return [StatusCode.COMMAND_ERR, "cooldown hasn't finished"]
	if game_self.spend(
		int(data.stats.deploy_cost * game_self.shop_discount), data.stats.income_impact
	):
		game_other.summon_enemy.emit(data)
	else:
		return [StatusCode.COMMAND_ERR, "doesn't have enough money"]
	return [StatusCode.OK]


func _get_unit_cooldown(_type: EnemyType) -> Array:
	var result: float = 0
	if game_other.enemy_cooldown.has(_type):
		result = game_other.enemy_cooldown[_type].get_time_left()
	return [StatusCode.OK, result]


func _get_enemy_info(enemy: Area2D) -> Dictionary:
	var type: EnemyType = enemy.type
	var data: Dictionary = {}
	var map = game_self.get_node("Map")
	if not map:
		return {}

	var pos: Vector2i = map.global_to_cell(enemy.path_follow.global_position)
	data["type"] = type
	data["position"] = {"x": pos[0], "y": pos[1]}
	data["progress_ratio"] = enemy.path_follow.progress_ratio
	data["income_impact"] = enemy.income_impact
	data["health"] = enemy.health
	data["max_health"] = enemy.max_health
	data["damage"] = enemy.damage
	data["max_speed"] = enemy.max_speed
	data["flying"] = enemy.flying
	data["knockback_resist"] = enemy.knockback_resist
	data["kill_reward"] = enemy.kill_reward

	return data


func _get_all_enemies(_owned: bool) -> Array:
	var enemies: Array
	if _owned:
		enemies = game_self.get_all_enemies()
	else:
		enemies = game_other.get_all_enemies()
	var enemies_info: Array = []

	for enemy in enemies:
		var enemy_info: Dictionary = _get_enemy_info(enemy)
		if enemy_info == {}:
			return [StatusCode.INTERNAL_ERR, []]
		enemies_info.push_back(enemy_info)

	return [StatusCode.OK, enemies_info]


#endregion

#region Spell


#gdlint: disable=max-returns
func _cast_spell(_type: SpellType, _coord: Vector2i) -> Array:
	var global_pos: Vector2 = game_self.map.cell_to_global(_coord)
	var spell_manager: Node = game_self.get_node("SpellManager")

	if spell_manager == null:
		push_error("[Agent] Node not found spell_manager")
		return [StatusCode.INTERNAL_ERR]

	var spell_node: Node = null
	match _type:
		SpellType.DOUBLE_INCOME:
			spell_node = spell_manager.get_node("DoubleIncome")
		SpellType.POISON:
			spell_node = spell_manager.get_node("Poison")
		SpellType.TELEPORT:
			spell_node = spell_manager.get_node("Teleport")
		_:
			push_error("[Agent] Unknown spell type:", _type)
			return [StatusCode.ILLEGAL_ARGUMENT]

	if spell_manager == null:
		push_error("[Agent] Node not found: SpellManager")
		return [StatusCode.INTERNAL_ERR, "Node not found SpellManager"]

	if _type == SpellType.DOUBLE_INCOME:
		if spell_node.is_on_cooldown or spell_node.is_active or not spell_node.game:
			return [StatusCode.CLIENT_ERR, "Spell is on cooldown"]
		var suc = spell_node.cast_spell()
		if not suc:
			push_error("[Agent] Cannot cast the spell for unknown reason")
			return [StatusCode.INTERNAL_ERR, "Cannot cast spell for unknown reason"]
	else:
		if spell_node.is_on_cooldown or not spell_node.game:
			return [StatusCode.CLIENT_ERR, "Spell is on cooldown"]
		var suc = spell_node.cast_spell(global_pos)
		if not suc:
			push_error("[Agent] Cannot cast the spell for unknown reason")
			return [StatusCode.INTERNAL_ERR, "Cannot cast spell for unknown reason"]

	return [StatusCode.OK]


func _get_spell_cooldown(_owned: bool, _type: SpellType) -> Array:
	var spell_manager: Node
	if _owned:
		spell_manager = game_self.get_node("SpellManager")
	else:
		spell_manager = game_other.get_node("SpellManager")

	if spell_manager == null:
		push_error("[Agent] Node not found: SpellManager")
		return [StatusCode.INTERNAL_ERR, -1]

	var spell_node_name = ""
	match _type:
		SpellType.DOUBLE_INCOME:
			spell_node_name = "DoubleIncome"
		SpellType.POISON:
			spell_node_name = "Poison"
		SpellType.TELEPORT:
			spell_node_name = "Teleport"
		_:
			push_error("[Agent] Unknown spell type: ", _type)
			return [StatusCode.ILLEGAL_ARGUMENT]

	var spell_node: Node = spell_manager.get_node(spell_node_name)
	if spell_node == null:
		push_error("[Agent] Node not found: %s" % spell_node_name)
		return [StatusCode.INTERNAL_ERR, -1]

	return [StatusCode.OK, spell_node.cooldown_timer.get_time_left()]


#endregion

#region Chat


func _get_screen_name_label() -> Label:
	if player_id == 1:
		return ongoing_round.get_node("Screen/Top/TextureRect/PlayerNameLeft")
	return ongoing_round.get_node("Screen/Top/TextureRect/PlayerNameRight")


func _send_chat(msg: String) -> Array:
	if chat_node == null:
		push_error("[Agent] TEXTBOX_SCENE is not loaded")
		return [StatusCode.INTERNAL_ERR, "TEXTBOX_SCENE is not loaded"]

	if chat_node.is_cool_down(player_id):
		return [StatusCode.COMMAND_ERR, "Cooldown hasn't finished"]

	if !send_pixelcat && msg.length() > 50:
		return [StatusCode.ILLEGAL_ARGUMENT, "Message is too long"]

	var chat_name_color = game_self.chat_name_color
	var player_name = _get_screen_name_label().text
	chat_node.send_chat_with_sender(player_id, msg, chat_name_color, player_name, send_pixelcat)
	game_self.chat_total_length += msg.length()
	return [StatusCode.OK]


func _pixel_cat() -> Array:
	if pixelcat_cnt == 0:
		return [StatusCode.COMMAND_ERR, "No more pixel cat!"]
	pixelcat_cnt -= 1
	send_pixelcat = true
	self._send_chat("[font_size=6]" + pixel_cat_str + "[/font_size]")
	send_pixelcat = false
	return [StatusCode.OK, pixel_cat_str]


func _get_chat_history(_num: int) -> Array:
	if chat_node == null:
		push_error("[Agent] TEXTBOX_SCENE is not loaded")
		return [StatusCode.INTERNAL_ERR, "TEXTBOX_SCENE is not loaded"]
	var history = chat_node.get_history(player_id, _num)
	return [StatusCode.OK, history]


func _set_chat_name_color(_color: String) -> Array:
	game_self.chat_name_color = _color
	return [StatusCode.OK]


#endregion

#region Misc


func get_label_str_len(label: Label, s: String, font_size: int) -> Vector2:
	var font = label.get_theme_font("font")
	return font.get_string_size(s, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)


func _set_name(_name: String) -> Array:
	var label = _get_screen_name_label()
	if get_label_str_len(label, _name, 50).x > 340:
		return [StatusCode.ILLEGAL_ARGUMENT, "Name is too long"]
	label.text = _name
	game_self.player_selection.get_node("PlayerIdentifierLabel").text = name
	return [StatusCode.OK]


#endregion

#region Premium-API


func _disconnect() -> Array:
	return [StatusCode.OK]


func _ntu_student_id_card() -> Array:
	game_self.shop_discount = 0.9
	var num: int = (randi() % 800) + 200
	var id: String = "B14902%d" % num
	return [StatusCode.OK, id]


func _metal_pipe() -> Array:
	AudioManager.play_metal_pipe()
	return [StatusCode.OK]


func _spam(_message: String, size: int) -> Array:
	game_self.send_danmaku(_message, size)
	return [StatusCode.OK]


func _super_star() -> Array:
	return [StatusCode.OK]


func _turbo_on() -> Array:
	return [StatusCode.OK]

#endregion
