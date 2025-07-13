class_name Round
extends Control

const GAME_DURATION = 300.0
const FREEZE_TIME = 60.0
const FREEZE_ANIMATION = 2.5

@export var game_timer_label: Label
@export var score_bar: ScoreBar
@export var game_1p: Game
@export var game_2p: Game

var manual_controlled: int

@onready var game_timer: Timer = $GameTimer


func set_controllers(
	player_selection_1p: IndividualPlayerSelection,
	player_selection_2p: IndividualPlayerSelection,
	_manual_controlled: int
) -> void:
	game_1p.set_controller(player_selection_1p)
	game_2p.set_controller(player_selection_2p)
	manual_controlled = _manual_controlled
	$Screen/Top/TextureRect/PlayerNameLeft.text = player_selection_1p.player_identifier
	$Screen/Top/TextureRect/PlayerNameRight.text = player_selection_2p.player_identifier

	# notify web agents
	player_selection_1p.web_agent.start_game(self, game_1p, game_2p)
	player_selection_2p.web_agent.start_game(self, game_2p, game_1p)


func set_maps(map: PackedScene):
	game_1p.set_map(map)
	game_2p.set_map(map)


func _ready() -> void:
	game_1p.op_game = game_2p
	game_2p.op_game = game_1p

	# start game timer
	game_timer.wait_time = GAME_DURATION
	game_timer.one_shot = true
	game_timer.start()

	# notify the shop and the chat
	var shop = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Shop
	var chat = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Chat
	match manual_controlled:
		0:
			shop.queue_free()
			chat.find_child("Shop").add_theme_color_override("font_color", Color(.6, .6, .6))
			chat.always_visible = true
		1:
			shop.start_game(game_1p, game_2p)
		2:
			shop.start_game(game_2p, game_1p)

	# setup signals for the games
	game_1p.damage_taken.connect(game_2p.on_damage_dealt)
	game_2p.damage_taken.connect(game_1p.on_damage_dealt)

	var agent_1p = game_1p.player_selection.web_agent
	var agent_2p = game_2p.player_selection.web_agent
	agent_1p.chat_node = chat
	agent_2p.chat_node = chat
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
	score_bar.left_score = game_1p.internal_score
	score_bar.right_score = game_2p.internal_score

	var time_after_freeze = FREEZE_TIME - $GameTimer.time_left
	if time_after_freeze >= 0:
		var frozen_overlay = $Screen/Top/TextureRect/FrozenOverlay
		frozen_overlay.visible = true
		frozen_overlay.modulate = Color(1, 1, 1, min(1.0, time_after_freeze / FREEZE_ANIMATION))

		game_1p.freeze()
		game_2p.freeze()
		$Screen/Top/TextureRect/Score.freeze()


func _on_game_timer_timeout():
	game_1p.player_selection.web_agent.game_running = false
	game_2p.player_selection.web_agent.game_running = false
	# load end scene
	var end_scene: EndScreen = preload("res://scenes/end.tscn").instantiate()
	end_scene.player_names = [
		$Screen/Top/TextureRect/PlayerNameLeft.text,
		$Screen/Top/TextureRect/PlayerNameRight.text,
	]
	end_scene.statistics = [
		EndScreen.Statistics.init("Score", [game_1p.internal_score, game_2p.internal_score], true),
		EndScreen.Statistics.init("Kill Count", [game_1p.kill_count, game_2p.kill_count], false),
		EndScreen.Statistics.init(
			"Total Money Earned", [game_1p.money_earned, game_2p.money_earned], true
		),
		EndScreen.Statistics.init(
			"Towers Built", [game_1p.tower_built, game_2p.tower_built], false
		),
		EndScreen.Statistics.init("Enemies Sent", [game_1p.enemy_sent, game_2p.enemy_sent], false),
		EndScreen.Statistics.init(
			"API Call Attempts", [game_1p.api_called, game_2p.api_called], false, true, true
		),
		EndScreen.Statistics.init(
			"API Call Failures",
			[game_1p.api_called - game_1p.api_succeed, game_2p.api_calledd - game_2p.api_succeed],
			false,
			true,
			true
		),
	]
	get_tree().get_root().add_child(end_scene)
	queue_free()
