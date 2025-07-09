class_name Round
extends Control

const GAME_DURATION = 10.0

@export var game_timer_label: Label
@export var score_bar: ScoreBar
@export var game_1p: Game
@export var game_2p: Game

var manual_controlled: int


func set_controllers(
	player_selection_1p: IndividualPlayerSelection,
	player_selection_2p: IndividualPlayerSelection,
	_manual_controlled: int
) -> void:
	manual_controlled = _manual_controlled

	# notify web agents
	player_selection_1p.web_agent.start_game(self, game_1p, game_2p)
	player_selection_2p.web_agent.start_game(self, game_2p, game_1p)


func _ready() -> void:
	$Screen/Bottom/LeftGame.op_game = $Screen/Bottom/RightGame
	$Screen/Bottom/RightGame.op_game = $Screen/Bottom/LeftGame
	$GameTimer.wait_time = GAME_DURATION
	$GameTimer.one_shot = true
	$StageSwitchTimer.wait_time = GAME_DURATION * 0.7
	$GameTimer.start()

	# notify web agents
	game_1p.find_child("RemoteAgent").start_game(self, game_1p, game_2p)
	game_2p.find_child("RemoteAgent").start_game(self, game_2p, game_1p)

	# notify the shop and the chat
	var shop = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Shop
	var chat = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Chat
	match manual_controlled:
		0:
			shop.queue_free()
			chat.always_visible = true
		1:
			shop.start_game(game_1p, game_2p)
		2:
			shop.start_game(game_2p, game_1p)

	# setup signals for the games
	game_1p.damage_taken.connect(game_2p.on_damage_dealt)
	game_2p.damage_taken.connect(game_1p.on_damage_dealt)
	var chat_node = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Chat
	var agent_1p = game_1p.find_child("RemoteAgent")
	var agent_2p = game_2p.find_child("RemoteAgent")
	agent_1p.chat_node = chat_node
	agent_2p.chat_node = chat_node
	agent_1p.player_id = 1
	agent_2p.player_id = 2
	AudioManager.background_game_stage1.play()


func get_formatted_time() -> String:
	var time_left = $GameTimer.time_left
	var minutes = int(time_left / 60)
	var seconds = int(time_left) % 60
	return "%02d:%02d" % [minutes, seconds]


func _process(_delta: float) -> void:
	game_timer_label.text = get_formatted_time()
	score_bar.left_score = game_1p.score
	score_bar.right_score = game_2p.score


func _on_game_timer_timeout():
	# load end scene
	var end_scene = preload("res://scenes/end.tscn").instantiate()
	end_scene.player1_score = game_1p.score
	end_scene.player2_score = game_2p.score
	# TODO: send real kill count stats
	end_scene.player1_kill_cnt = game_1p.kill_cnt
	end_scene.player2_kill_cnt = game_2p.kill_cnt
	end_scene.player1_money = game_1p.money
	end_scene.player2_money = game_2p.money
	get_tree().get_root().add_child(end_scene)
	queue_free()
