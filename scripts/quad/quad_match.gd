extends Control

var config: Dictionary
var the_rounds: Array[Round]

# keys: player names
# values: a dictionary of (stat, value). entries include "win", "lose",
# "draw", "score_diff", and every entry in end_scene.statistics
var round_results: Dictionary = {}
var result_path: String

@onready var subviewports: Array[SubViewport] = [
	$SubViewportContainerNw/SubViewport,
	$SubViewportContainerNe/SubViewport,
	$SubViewportContainerSw/SubViewport,
	$SubViewportContainerSe/SubViewport,
]


func init(config_path: String, _config: Dictionary, _the_rounds: Array[Round]) -> void:
	config = _config
	the_rounds = _the_rounds
	result_path = get_result_path(config_path)


func _ready() -> void:
	for i in range(4):
		the_rounds[i].game_finished.connect(collect_result.bind(i))
		subviewports[i].add_child(the_rounds[i])
	add_child(preload("res://scenes/pause_menu.tscn").instantiate())


func get_result_path(config_path: String) -> String:
	var length = config_path.length()
	var it: int = length - 1
	while config_path[it - 1] != "/":
		it -= 1
	return "%sresult-%s" % [config_path.substr(0, it), config_path.substr(it, length - it)]


func collect_result(stats: Array[EndScreen.Statistics], round_id: int) -> void:
	var stat_left: Dictionary = {}
	var stat_right: Dictionary = {}
	for stat: EndScreen.Statistics in stats:
		stat_left[stat.title] = stat.player_scores[0]
		stat_right[stat.title] = stat.player_scores[1]

	# determine winning side
	var winning_side = 0
	if stat_left["Score"] > stat_right["Score"]:
		winning_side = 1
	elif stat_left["Score"] < stat_right["Score"]:
		winning_side = 2
	elif stat_left["Total Money Earned"] > stat_right["Total Money Earned"]:
		winning_side = 1
	elif stat_left["Total Money Earned"] < stat_right["Total Money Earned"]:
		winning_side = 2

	stat_left["win"] = (winning_side == 1) as int
	stat_right["win"] = (winning_side == 2) as int
	stat_left["lose"] = stat_right["win"]
	stat_right["lose"] = stat_left["win"]
	stat_left["draw"] = (winning_side == 0) as int
	stat_right["draw"] = (winning_side == 0) as int
	stat_left["score_diff"] = stat_left["Score"] - stat_right["Score"]
	stat_right["score_diff"] = stat_right["Score"] - stat_left["Score"]

	var key = ["nw", "ne", "sw", "se"][round_id]
	var pid_left = config[key]["player-left"]["id"]
	var pid_right = config[key]["player-right"]["id"]
	round_results.set(pid_left, stat_left)
	round_results.set(pid_right, stat_right)

	if round_results.size() == 8:
		Util.save_json(result_path, round_results)

# TODO: focus one game
