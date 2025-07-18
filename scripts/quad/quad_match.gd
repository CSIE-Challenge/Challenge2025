extends Control

var config: Dictionary
var the_rounds: Array[Round]

# keys: player names
# values: a dictionary of (stat, value). entries include "win", "lose",
# "draw", "score_diff", and every entry in end_scene.statistics
var round_results: Dictionary = {}
var result_path: String
var result_to_collect: int

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
	if len(the_rounds) == 1:
		$SubViewportContainerNw.scale = Vector2(1, 1)
		# $SubViewportContainerNw.anchor_right = 1
		# $SubViewportContainerNw.anchor_bottom = 1
		$SubViewportContainerNe.visible = false
		$SubViewportContainerSw.visible = false
		$SubViewportContainerSe.visible = false
		the_rounds[0].reveal_cutscene = true
	result_to_collect = len(the_rounds)
	for i in range(len(the_rounds)):
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
	if not round_results.has(pid_left):
		round_results.set(pid_left, stat_left)
	else:
		for k in stat_left.keys():
			round_results[pid_left][k] += stat_left[k]
	if not round_results.has(pid_right):
		round_results.set(pid_right, stat_right)
	else:
		for k in stat_right.keys():
			round_results[pid_right][k] += stat_right[k]

	result_to_collect -= 1
	if result_to_collect == 0:
		Util.save_json(result_path, round_results)

# TODO: focus one game
