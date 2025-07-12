class_name Agent
extends Node
enum GameStatus { PREPARE, START, READY, END }
enum AgentType { HUMAN, AI, NIL }
# TODO: Remove BASIC legacy
enum TowerType { BASIC, DONKEY_KONG, FIRE_MARIO, FORT, ICE_LUIGI, SHY_GUY }
enum EnemyType {
	BUZZY_BEETLE,
	GOOMBA,
	KOOPA_JR,
	KOOPA_PARATROOPA,
	KOOPA,
	SPINY_SHELL,
	WIGGLER,
}
enum SpellType { POISON = 1, DOUBLE_INCOME = 2, TELEPORT = 3 }
enum StatusCode {
	OK = 200,
	ILLFORMED_COMMAND = 400,
	AUTH_FAIL = 401,
	ILLEGAL_ARGUMENT = 402,
	COMMAND_ERR = 403,
	NOT_FOUND = 404,
	TOO_FREQUENT = 405,
	NOT_STARTED = 406,
	INTERNAL_ERR = 500,
	CLIENT_ERR = 501
}

const TOWER_SCENES = [
	[preload("res://scenes/towers/twin_turret.tscn")],
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
var type: AgentType = AgentType.NIL
var game_status: GameStatus = GameStatus.PREPARE
var money: int
var score: int
var player_id: int

var game_running: bool = false
var ongoing_round: Round = null
var game_self: Game = null
var game_other: Game = null
var chat_node: Node = null

var sys_paths: Array = [[], []]
var opp_paths: Array = [[], []]


func start_game(_round: Round, _game_self: Game, _game_other: Game) -> void:
	game_running = true
	ongoing_round = _round
	game_self = _game_self
	game_other = _game_other


#region MapInfo


func _get_all_terrain() -> Array:
	print("[GetAllTerrain] Get request")
	var map = game_self.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "[GetAllTerrain] Error: cannot find map"]

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


func _get_terrain(_owned: bool, _coord: Vector2i) -> Array:
	print("[GetTerrain] Get request")
	var map
	if _owned == true:
		map = game_self.get_node("Map")
	else:
		map = game_other.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "[GetAllTerrain] Error: cannot find map"]

	return [StatusCode.OK, map.get_cell_terrain(_coord)]


func _get_scores(_owned: bool) -> Array:
	print("[GetScores] Get request")
	var result: int
	if _owned == true:
		result = game_self.score
	else:
		result = game_other.score
	return [StatusCode.OK, result]


func _get_current_wave() -> Array:
	print("[GetCurrentWave] Get request")
	var wave = ongoing_round.get_node("Spawner")
	if not wave:
		return [StatusCode.INTERNAL_ERR, "[GetCurrentWave] Error: cannot find wave"]
	var wave_num: int = wave.current_wave_data.wave_number
	return [StatusCode.OK, wave_num]


func _get_remain_time() -> Array:
	print("[GetRemainTime] Get request")
	if not game_running:
		# TODO: get remaining time from player_selection when counting down
		return [StatusCode.OK, 1]
	var time_left = ongoing_round.get_node("GameTimer").time_left
	if time_left == null:
		return [StatusCode.INTERNAL_ERR, "[GetRemainTime] Error: cannot find timeleft"]
	return [StatusCode.OK, time_left]


func _get_time_until_next_wave() -> Array:
	print("[GetTimeUntilNextWave] Get request")
	var time_left = ongoing_round.get_node("Spawner").next_wave_timer.time_left
	if time_left == null:
		return [
			StatusCode.INTERNAL_ERR,
			"[GetTimeUntilNextWave] Error: cannot find timeleft till next wave"
		]
	return [StatusCode.OK, time_left]


func _get_money(_owned: bool) -> Array:
	print("[GetMoney] Get request")
	var result: int
	if _owned == true:
		result = int(game_self.status_panel.find_child("Money").text)
	else:
		result = int(game_other.status_panel.find_child("Money").text)
	return [StatusCode.OK, result]


func _get_income(_owned: bool) -> Array:
	print("[GetIncome] Get request")
	var income: int
	if _owned == true:
		income = int(game_self.status_panel.find_child("Income").text)
	else:
		income = int(game_other.status_panel.find_child("Income").text)
	return [StatusCode.OK, income]


func _get_game_status() -> Array:
	return [StatusCode.OK, game_status]


func _get_system_path(_fly: bool) -> Array:
	var map: Map = game_self._map
	if not map:
		return [StatusCode.INTERNAL_ERR, "[GetSystemPath] Error: cannot find map"]

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
	var map: Map = game_self._map
	if not map:
		return [StatusCode.INTERNAL_ERR, "[GetSystemPath] Error: cannot find map"]

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
	print(end_cell)
	if end_cell not in opp_paths[index]:
		opp_paths[index].append(end_cell)
	return [StatusCode.OK, opp_paths[index]]


#endregion

#region Tower


func _place_tower(_type: TowerType, _level: String, _coord: Vector2i) -> Array:
	print("[PlaceTower] Get request")
	var map = game_self.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "[PlaceTower] Error: cannot find map"]
	if map.get_cell_terrain(_coord) != Map.CellTerrain.EMPTY:
		return [StatusCode.COMMAND_ERR, "[PlaceTower] Error: invalid coordinate for building tower"]

	if (not _type in range(0, 6)) or (not _level in LEVEL_TO_INDEX.keys()):
		return [
			StatusCode.ILLEGAL_ARGUMENT,
			"[PlaceTower] Error: 'type' out of range or 'level' invalid"
		]

	var tower = TOWER_SCENES[_type][LEVEL_TO_INDEX[_level]].instantiate()
	if game_self.built_towers.has(_coord):
		var previous_tower = game_self.built_towers[_coord]
		if (
			(
				previous_tower.type == tower.type
				and (
					previous_tower.level_a > tower.level_a or previous_tower.level_b > tower.level_b
				)
			)
			or money + previous_tower.building_cost < tower.building_cost
		):
			return [StatusCode.COMMAND_ERR, "[PlaceTower] Error: can't upgrade tower"]
		if (
			previous_tower.type != tower.type
			and (
				game_self.money + (previous_tower.building_cost * game_self.DEPRECIATION_RATE)
				< tower.building_cost
			)
		):
			print(previous_tower.building_cost, tower.building_cost)
			return [StatusCode.COMMAND_ERR, "[PlaceTower] Error: no enough money"]
	game_self.place_tower(_coord, tower)
	return [StatusCode.OK]


func _get_all_towers(_owned: bool) -> Array:
	print("[GetAllTowers] Get request")
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


func _get_tower(_coord: Vector2i) -> Array:
	print("[GetTower] Get request")
	if game_self.built_towers.has(_coord):
		var dict = game_self.built_towers[_coord].to_dict(_coord)
		return [StatusCode.OK, dict]
	if game_other.built_towers.has(_coord):
		var dict = game_other.built_towers[_coord].to_dict(_coord)
		return [StatusCode.OK, dict]
	return [StatusCode.OK, {}]


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
	print("[SpawnUnit] Get request")
	var data = _get_unit_dict(_type)
	if game_self.spend(data.stats.deploy_cost, data.stats.income_impact):
		game_other.summon_enemy.emit(data)
	else:
		print("[Error] doesn't have enough money")
		return [StatusCode.COMMAND_ERR]
	return [StatusCode.OK]


func _get_enemy_info(enemy: Area2D) -> Dictionary:
	var type: EnemyType = enemy.type
	var data: Dictionary = {}
	var map = game_self.get_node("Map")
	if not map:
		return {}

	data["type"] = type
	data["income_impact"] = enemy.income_impact
	data["max_health"] = enemy.max_health
	data["max_speed"] = enemy.max_speed
	data["damage"] = enemy.damage
	data["flying"] = enemy.flying
	data["knockback_resist"] = enemy.knockback_resist
	data["kill_reward"] = enemy.kill_reward
	data["health"] = enemy.health
	data["progress_ratio"] = enemy.path_follow.progress_ratio

	var pos: Vector2i = map.global_to_cell(enemy.path_follow.global_position)
	data["position"] = {"x": pos[0], "y": pos[1]}
	print(data)
	return data


func _get_available_units() -> Array:
	print("[GetAvailableEnemies] Get request")
	return [StatusCode.OK]


func _get_all_enemies() -> Array:
	print("[GetAllEnemies] Get request")
	var enemies: Array = game_self.get_all_enemies()
	var enemies_info: Array = []

	for enemy in enemies:
		var enemy_info: Dictionary = _get_enemy_info(enemy)
		if enemy_info == {}:
			return [StatusCode.INTERNAL_ERR, []]
		enemies_info.push_back(enemy_info)

	return [StatusCode.OK, enemies_info]


#endregion

#region Spell


func _cast_spell(_type: SpellType, _coord: Vector2i) -> Array:
	var global_pos: Vector2 = game_self._map.cell_to_global(_coord)
	print("[CastSpell] Get request")
	var spell_manager: Node = game_self.get_node("SpellManager")

	if spell_manager == null:
		print("[ERROR] node not found spell_manager")
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
			print("[Error] Unknown spell type:", _type)
			return [StatusCode.ILLEGAL_ARGUMENT]

	if spell_manager == null:
		print("[ERROR] node not found spell_manager")
		return [StatusCode.INTERNAL_ERR]

	if _type == SpellType.DOUBLE_INCOME:
		var suc = spell_node.cast_spell()
		print(suc)
		if not suc:
			print("[ERROR] cann't cast the spell")
			return [StatusCode.CLIENT_ERR]
	else:
		var suc = spell_node.cast_spell(global_pos)
		if not suc:
			print("[ERROR] cann't cast the spell")
			return [StatusCode.CLIENT_ERR]

	return [StatusCode.OK]


func _get_spell_cooldown(_owned: bool, _type: SpellType) -> Array:
	print("[GetSpellCooldown] Get request")
	var spell_manager: Node
	if _owned:
		spell_manager = game_self.get_node("SpellManager")
	else:
		spell_manager = game_other.get_node("SpellManager")

	if spell_manager == null:
		print("[ERROR] node not found spell_manager")
		return [StatusCode.INTERNAL_ERR, -1]

	var spell_node: Node = null
	match _type:
		SpellType.DOUBLE_INCOME:
			spell_node = spell_manager.get_node("DoubleIncome")
		SpellType.POISON:
			spell_node = spell_manager.get_node("Poison")
		SpellType.TELEPORT:
			spell_node = spell_manager.get_node("Teleport")
		_:
			print("[Error] Unknown spell type:", _type)
			return [StatusCode.ILLEGAL_ARGUMENT]

	if spell_node == null:
		print("[ERROR] node not found spell")
		return [StatusCode.INTERNAL_ERR, -1]

	return [StatusCode.OK, spell_node.cooldown_timer.get_time_left()]


func _get_spell_cost(_type: SpellType) -> Array:
	print("[GetAllSpellCost] Get request")
	var spell_manager: Node = game_self.get_node("SpellManager")

	if spell_manager == null:
		print("[ERROR] node not found spell_manager")
		return [StatusCode.INTERNAL_ERR, -1]

	var spell_node: Node = null
	match _type:
		SpellType.DOUBLE_INCOME:
			spell_node = spell_manager.get_node("DoubleIncome")
		SpellType.POISON:
			spell_node = spell_manager.get_node("Poison")
		SpellType.TELEPORT:
			spell_node = spell_manager.get_node("Teleport")
		_:
			print("[Error] Unknown spell type:", _type)
			return [StatusCode.ILLEGAL_ARGUMENT]

	if spell_node == null:
		print("[ERROR] node not found spell")
		return [StatusCode.INTERNAL_ERR, -1]

	return [StatusCode.OK, spell_node.metadata.stats.cost]


#func _get_effective_spells(_owned: bool) -> Array:
#	print("[GetEffectiveSpells] Get request")
#	return [StatusCode.OK]
#
#
#func spell_to_dict(spell_node:Node, type:SpellType) -> dict:
#	var ret = {}
#	if type == SpellType.DoubleIncome:
#		ret["range"] = 0
#		ret["damage"] = 0
#	else:
#		ret["range"] = spell_node.metadata.stats.radius
#		ret["damage"] = spell_node.metadata.stats.
#
#	ret["type"] = type
#	ret["duration"] = spell_node.metadata.stats.duration

#endregion

#region Chat


func _send_chat(_msg: String) -> Array:
	print("[SendChat] Get request")
	if chat_node == null:
		print("[Error] TEXTBOX_SCENE not loaded")
		return [StatusCode.INTERNAL_ERR, false]

	if _msg.length() > 50:
		print("[Error] too long")
		return [StatusCode.ILLEGAL_ARGUMENT, false]

	chat_node.send_chat_with_sender(player_id, _msg)
	return [StatusCode.OK, true]


func _get_chat_history(_num: int) -> Array:
	print("[GetChatHistory] Get request")
	if chat_node == null:
		print("[Error] TEXTBOX_SCENE not loaded")
		return [StatusCode.INTERNAL_ERR, false]

	var history = chat_node.get_history(_num)
	return [StatusCode.OK, history]

#endregion
