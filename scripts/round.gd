class_name Round
extends Control

const GAME_DURATION = 180.0

@export var game_timer_label: Label
@export var score_bar: ScoreBar
@export var game_1p: Game
@export var game_2p: Game


func _ready() -> void:
	$GameTimer.wait_time = GAME_DURATION
	$GameTimer.one_shot = true
	$StageSwitchTimer.wait_time = GAME_DURATION * 0.7
	$GameTimer.start()
	$StageSwitchTimer.start()
	game_1p.find_child("RemoteAgent").start_game(self, game_1p, game_2p)
	game_2p.find_child("RemoteAgent").start_game(self, game_2p, game_1p)
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


func _on_stage_change() -> void:
	AudioManager.background_game_stage1.stop()
	AudioManager.background_game_stage2.play()
