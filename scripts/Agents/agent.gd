class_name Agent
extends Node
enum GameStatus { PREPARE, START, READY, END }
enum AgentType { HUMAN, AI, NIL }
# TODO: Remove BASIC legacy
enum TowerType { BASIC, DONKEY_KONG, FIRE_MARIO, FORT, ICE_LUIGI, SHY_GUY }
enum EnemyType { BASIC }
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
	INTERNAL_ERR = 500,
	CLIENT_ERR = 501
}

const TOWER_SCENE := preload("res://scenes/towers/twin_turret.tscn")
const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")
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
	var score: int
	if _owned == true:
		score = game_self.score
	else:
		score = game_other.score
	return [StatusCode.OK, score]


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
	var money: int
	if _owned == true:
		money = int(game_self.status_panel.find_child("Money").text)
	else:
		money = int(game_other.status_panel.find_child("Money").text)
	return [StatusCode.OK, money]


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


#endregion

#region Tower


func _place_tower(_type: TowerType, _level_a: int, _level_b: int, _coord: Vector2i) -> Array:
	print("[PlaceTower] Get request")
	if _type == TowerType.BASIC:
		return [StatusCode.OK]
	var map = game_self.get_node("Map")
	if not map:
		return [StatusCode.INTERNAL_ERR, "[PlaceTower] Error: cannot find map"]
	if map.get_cell_terrain(_coord) != Map.CellTerrain.EMPTY:
		return [StatusCode.COMMAND_ERR, "[PlaceTower] Error: invalid coordinate for building tower"]
	var index: int = -1
	if _level_a == 1:
		if _level_b == 1:
			index = 0
		elif _level_b == 2:
			index = 2
		elif _level_b == 3:
			index = 4
	elif _level_a == 2 and _level_b == 1:
		index = 1
	elif _level_a == 3 and _level_b == 1:
		index = 3
	if index == -1:
		return [StatusCode.COMMAND_ERR, "[PlaceTower] Error: invalid level"]
	var tower_data = TowerData.new()
	var new_tower_scene = load(tower_data.tower_data_list[(_type - 1) * 5 + index])
	game_self.place_tower(_coord, new_tower_scene.instantiate())
	return [StatusCode.OK]


func _get_all_towers(_owned: bool) -> Array:
	print("[GetAllTowers] Get request")
	var towers: Array = []
	if _owned:
		for key in game_self.built_towers.keys():
			var tower_dict = game_self.built_towers[key].to_dict(key)
			tower_dict["type"] = TowerType.BASIC
			towers.append(tower_dict)
		return [StatusCode.OK, towers]
	for key in game_other.built_towers.keys():
		var tower_dict = game_other.built_towers[key].to_dict(key)
		tower_dict["type"] = TowerType.BASIC
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
	return [StatusCode.INTERNAL_ERR, "[GetTower] Error: no tower found"]


#endregion

#region Enemy


func _spawn_enemy(_type: EnemyType) -> Array:
	print("[SpawnEnemy] Get request")
	return [StatusCode.OK]


func _get_enemy_cooldown(_owned: bool, _type: EnemyType) -> Array:
	print("[GetEnemyCooldown] Get request")
	return [StatusCode.OK]


func _get_enemy_info(_type: EnemyType) -> Array:
	print("[GetAllEnemyInfo] Get request")
	return [StatusCode.OK]


func _get_available_enemies() -> Array:
	print("[GetAvailableEnemies] Get request")
	return [StatusCode.OK]


func _get_closest_enemies(_position: Vector2i, _count: int) -> Array:
	print("[GetClosestEnemies] Get request")
	return [StatusCode.OK]


func _get_enemies_in_range(_center: Vector2i, _radius: float) -> Array:
	print("[GetEnemiesInRange] Get request")
	return [StatusCode.OK]


#endregion

#region Spell


func _cast_spell(_type: SpellType, _coord: Vector2i) -> Array:
	print("[CastSpell] Get request")
	return [StatusCode.OK]


func _get_spell_cooldown(_owned: bool, _type: SpellType) -> Array:
	print("[GetSpellCooldown] Get request")
	return [StatusCode.OK]


func _get_spell_cost() -> Array:
	print("[GetAllSpellCost] Get request")
	return [StatusCode.OK]


func _get_effective_spells(_owned: bool) -> Array:
	print("[GetEffectiveSpells] Get request")
	return [StatusCode.OK]


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
