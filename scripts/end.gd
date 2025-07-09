extends Node2D

# TODO: replace names and stats with real data
var player1_score = 11
var player1_kill_cnt = 4
var player1_money = 514

var player2_score = 19
var player2_kill_cnt = 19
var player2_money = 810


func _ready():
	# set winner
	var winner_name = "player1"
	if player2_score > player1_score:
		winner_name = "player2"
	elif player2_score == player1_score && player2_money > player1_money:
		winner_name = "player2"
	$winner_text.text = $winner_text.text.format({"name": winner_name})
	# set player 1 name
	var player1_name_str = $player_stats_1.get_node("player_name").text
	player1_name_str = player1_name_str.format({"name": "player1"})
	$player_stats_1.get_node("player_name").text = player1_name_str
	# set player 2 name
	var player2_name_str = $player_stats_2.get_node("player_name").text
	player2_name_str = player2_name_str.format({"name": "player2"})
	$player_stats_2.get_node("player_name").text = player2_name_str
	# set player 1 stats
	var player1_stats_str = $player_stats_1.get_node("player_stats").text
	player1_stats_str = player1_stats_str.format(
		{"score": player1_score, "kill_cnt": player1_kill_cnt, "money": player1_money}
	)
	$player_stats_1.get_node("player_stats").text = player1_stats_str
	# set player 2 stats
	var player2_stats_str = $player_stats_2.get_node("player_stats").text
	player2_stats_str = player2_stats_str.format(
		{"score": player2_score, "kill_cnt": player2_kill_cnt, "money": player2_money}
	)
	$player_stats_2.get_node("player_stats").text = player2_stats_str
