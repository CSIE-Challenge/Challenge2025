class_name Agent
extends Node

enum AgentType { HUMAN, AI, NIL }
enum TowerType { BASIC }
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
	INTERNAL_ERR = 500,
	CLIENT_ERR = 501
}

var type: AgentType = AgentType.NIL
var money: int
var score: int

@onready var game = self.get_parent()
@onready var round = game.get_parent()

#region MapInfo


func _get_all_terrain() -> Array:
	print("[GetAllTerrain] Get request")
	var map = game.get_node("Map")
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


func _get_scores(_owned: bool) -> Array:
	print("[GetScores] Get request")
	return [StatusCode.OK, 48763]


func _get_current_wave() -> Array:
	print("[GetCurrentWave] Get request")
	return [StatusCode.OK]


func _get_remain_time() -> Array:
	print("[GetRemainTime] Get request")
	var time_left = round.get_node("GameTimer").time_left
	if time_left == null:
		return [StatusCode.INTERNAL_ERR, "[GetRemainTime] Error: cannot find timeleft"]
	return [StatusCode.OK, time_left]


func _get_time_until_next_wave() -> Array:
	print("[GetTimeUntilNextWave] Get request")
	return [StatusCode.OK]


func _get_money(_owned: bool) -> Array:
	print("[GetMoney] Get request")
	return [StatusCode.OK]


func _get_income(_owned: bool) -> Array:
	print("[GetIncome] Get request")
	return [StatusCode.OK]


#endregion

#region Tower


func _place_tower(_type: TowerType, _coord: Vector2i) -> Array:
	print("[PlaceTower] Get request")
	return [StatusCode.OK]


func _get_all_towers(_owned: bool) -> Array:
	print("[GetAllTower] Get request")
	return [StatusCode.OK]


func _get_tower(_coord: Vector2i) -> Array:
	print("[GetTower] Get request")
	return [StatusCode.OK]


#endregion

#region Enemy


func _spawn_enemy(_type: EnemyType) -> Array:
	print("[SpawnEnemy] Get request")
	return [StatusCode.OK]


func _get_enemy_cooldown(_owned: bool, _type: EnemyType) -> Array:
	print("[GetEnemyCooldown] Get request")
	return [StatusCode.OK]


func _get_all_enemy_info(_type: EnemyType) -> Array:
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


func _get_all_spell_cost() -> Array:
	print("[GetAllSpellCost] Get request")
	return [StatusCode.OK]


func _get_effective_spells(_owned: bool) -> Array:
	print("[GetEffectiveSpells] Get request")
	return [StatusCode.OK]


#endregion

#region Chat


func _send_chat(_msg: String) -> Array:
	print("[SendChat] Get request")
	return [StatusCode.OK]


func _get_chat_history(_num: int) -> Array:
	print("[GetChatHistory] Get request")
	return [StatusCode.OK]

#endregion
