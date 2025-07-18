class_name Round
extends Control

signal game_finished(stats: Array[EndScreen.Statistics])

const GAME_DURATION = 300.0
const FREEZE_TIME = 60.0
const FREEZE_ANIMATION = 2.5

@export var game_timer_label: Label
@export var score_bar: ScoreBar
@export var game_1p: Game
@export var game_2p: Game
@export var spawner: Spawner

var manual_controlled: int

# when turned on, pressing ESC does not pause the game or exit the game on end screen
var system_controlled: bool = false

var reveal_cutscene: bool = false
var cutscene_timers = []

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


func set_maps(map: PackedScene):
	game_1p.set_map(map)
	game_2p.set_map(map)


func set_api_quotas(quota_1p: int, quota_2p: int) -> void:
	game_1p.premium_api_quota = quota_1p
	game_2p.premium_api_quota = quota_2p


func _ready() -> void:
	# Engine.time_scale = 5  # to comment
	game_1p.process_mode = Node.PROCESS_MODE_DISABLED
	game_2p.process_mode = Node.PROCESS_MODE_DISABLED
	spawner.process_mode = Node.PROCESS_MODE_DISABLED
	if not system_controlled:
		add_child(preload("res://scenes/pause_menu.tscn").instantiate())

	# init game timer
	game_timer.wait_time = GAME_DURATION
	game_timer.one_shot = true

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
			game_1p.is_manually_controlled = true
		2:
			shop.start_game(game_2p, game_1p)
			game_2p.is_manually_controlled = true

	var cutscene = $Cutscene
	var cutscene_rect = $Cutscene/ColorRect
	var cutscene_title = $Cutscene/ColorRect/TextureRect
	var cutscene_slogan = $Cutscene/ColorRect/Slogan
	if reveal_cutscene:
		cutscene.visible = true
		var create_timer = func(time: float, callback: Callable):
			var timer = Timer.new()
			add_child(timer)
			timer.wait_time = time
			timer.one_shot = true
			timer.timeout.connect(callback)
			timer.start()

		cutscene_rect.modulate = Color(0, 1, 0, 0)
		cutscene_slogan.modulate = Color(0, 1, 0, 0)
		cutscene_title.modulate = Color(1, 1, 1, 0)
		create_timer.call(
			5,
			func(): create_tween().tween_property(cutscene_rect, "modulate:a", 1.0, 3).set_delay(0)
		)
		create_timer.call(
			8,
			func():
				$Cutscene/MapRevealLeft.visible = false
				$Cutscene/MapRevealRight.visible = false
				$Cutscene/MapRevealLeft.clear_square()
				$Cutscene/MapRevealRight.clear_square()
				create_tween().tween_property(cutscene_rect, "modulate:r", 1.0, 2).set_delay(0)
				create_tween().tween_property(cutscene_rect, "modulate:b", 1.0, 2).set_delay(0)
		)
		create_timer.call(
			10,
			func(): create_tween().tween_property(cutscene_title, "modulate:a", 1.0, 2).set_delay(0)
		)
		create_timer.call(
			11,
			func():
				create_tween().tween_property(cutscene_slogan, "modulate:a", 1.0, 2).set_delay(0)
		)
		create_timer.call(
			14, func(): create_tween().tween_property(cutscene, "modulate:a", 0.0, 3).set_delay(0)
		)
		create_timer.call(18, _start)
	else:
		cutscene.process_mode = Node.PROCESS_MODE_DISABLED
		cutscene.visible = false

		_start()


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_SPACE:
		$Cutscene.visible = false
		_start()


func _start() -> void:
	if !game_timer.is_stopped():
		return
	# start game timer
	game_timer.start()

	game_1p.start()
	game_2p.start()
	spawner.process_mode = Node.PROCESS_MODE_PAUSABLE
	$Screen/Bottom/Mid/ShopAndChat.mouse_filter = MOUSE_FILTER_IGNORE

	spawner.start()
	# notify web agents
	game_1p.player_selection.web_agent.start_game(self, game_1p, game_2p)
	game_2p.player_selection.web_agent.start_game(self, game_2p, game_1p)

	game_1p.op_game = game_2p
	game_2p.op_game = game_1p
	$GPUParticles2D.visible = false

	# setup signals for the games
	game_1p.damage_taken.connect(game_2p.on_damage_dealt)
	game_2p.damage_taken.connect(game_1p.on_damage_dealt)

	var chat = $Screen/Bottom/Mid/ShopAndChat/TabContainer/Chat
	chat.start()
	var agent_1p = game_1p.player_selection.web_agent
	var agent_2p = game_2p.player_selection.web_agent
	agent_1p.chat_node = chat
	agent_2p.chat_node = chat
	agent_1p.player_id = 1
	agent_2p.player_id = 2
	AudioManager.background_game_stage1.play()

	for timer in cutscene_timers:
		timer.queue_free()


func get_formatted_time() -> String:
	var time_left = GAME_DURATION if game_timer.is_stopped() else game_timer.time_left
	var minutes = int(time_left / 60)
	var seconds = int(time_left) % 60
	return "%02d:%02d" % [minutes, seconds]


func _process(_delta: float) -> void:
	game_timer_label.text = get_formatted_time()
	score_bar.left_score = game_1p.score
	score_bar.right_score = game_2p.score

	if (
		!game_timer.is_stopped()
		and game_timer.time_left < GAME_DURATION * 0.3
		and not AudioManager.second_stage
	):
		AudioManager.second_stage = true
		AudioManager.background_game_stage1.stop()
		AudioManager.background_game_stage2.play()

	if !game_timer.is_stopped():
		var time_after_freeze = FREEZE_TIME - game_timer.time_left
		if time_after_freeze >= 0:
			var frozen_overlay = $Screen/Top/TextureRect/FrozenOverlay
			frozen_overlay.visible = true
			frozen_overlay.modulate = Color(1, 1, 1, min(1.0, time_after_freeze / FREEZE_ANIMATION))

			$GPUParticles2D.visible = true
			game_1p.freeze()
			game_2p.freeze()
			$Screen/Top/TextureRect/Score.freeze()


func _on_game_timer_timeout():
	game_1p.player_selection.web_agent.game_running = false
	game_2p.player_selection.web_agent.game_running = false
	# load end scene
	ApiServer.stop()
	var end_scene: EndScreen = preload("res://scenes/end.tscn").instantiate()
	end_scene.quit_hotkey_enabled = not system_controlled
	end_scene.player_names = [
		$Screen/Top/TextureRect/PlayerNameLeft.text,
		$Screen/Top/TextureRect/PlayerNameRight.text,
	]
	end_scene.statistics = [
		EndScreen.Statistics.init("Score", [game_1p.score, game_2p.score], true),
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
			[game_1p.api_called - game_1p.api_succeed, game_2p.api_called - game_2p.api_succeed],
			false,
			true,
			true
		),
	]
	AudioManager.background_game_stage2.stop()
	AudioManager.background_menu.play()
	get_parent().add_child(end_scene)
	queue_free()
	game_finished.emit(end_scene.statistics)
