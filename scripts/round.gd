class_name Round
extends Control

const GAME_DURATION = 180.0

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
	game_1p.set_controller(player_selection_1p)
	game_2p.set_controller(player_selection_2p)
	manual_controlled = _manual_controlled


func _ready() -> void:
	# start game timer
	$GameTimer.wait_time = GAME_DURATION
	$GameTimer.one_shot = true
	$GameTimer.start()

	# notify web agents
	game_1p.player_selection.web_agent.start_game(self, game_1p, game_2p)
	game_2p.player_selection.web_agent.start_game(self, game_2p, game_1p)

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


func get_formatted_time() -> String:
	var time_left = $GameTimer.time_left
	var minutes = int(time_left / 60)
	var seconds = int(time_left) % 60
	return "%02d:%02d" % [minutes, seconds]


func _process(_delta: float) -> void:
	game_timer_label.text = get_formatted_time()
	score_bar.left_score = game_1p.score
	score_bar.right_score = game_2p.score
