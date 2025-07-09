extends Node2D

# TODO: replace names and stats with real data


func _ready():
	$winner_text.text = $winner_text.text.format({"name": "ohya"})
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
	player1_stats_str = player1_stats_str.format({"score": 11, "kill_cnt": 4, "balance": 514})
	$player_stats_1.get_node("player_stats").text = player1_stats_str
	# set player 2 stats
	var player2_stats_str = $player_stats_2.get_node("player_stats").text
	player2_stats_str = player2_stats_str.format({"score": 19, "kill_cnt": 19, "balance": 810})
	$player_stats_2.get_node("player_stats").text = player2_stats_str
