extends Control

const ROUND_SCENE = preload("res://scenes/round.tscn")

@onready var selection_1p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection1P
@onready var selection_2p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection2P
@onready var game_start_button: Button = $VBoxContainer/StartButton
@onready var game_start_timer: Timer = $GameStartTimer


func _ready() -> void:
	selection_1p.manual_control_enabled.connect(func(): selection_2p.manual_control = false)
	selection_2p.manual_control_enabled.connect(func(): selection_1p.manual_control = false)


func _process(_delta: float) -> void:
	if not game_start_timer.is_stopped():
		game_start_button.text = "Starting in %d" % ceil(game_start_timer.time_left)


func _on_start_button_pressed() -> void:
	selection_1p.freeze()
	selection_2p.freeze()
	game_start_timer.start()


func _on_game_start_timer_timeout() -> void:
	var manual_controlled = 0
	if selection_1p.manual_control:
		manual_controlled = 1
	if selection_2p.manual_control:
		manual_controlled = 2

	var the_round = ROUND_SCENE.instantiate()
	get_tree().get_root().add_child(the_round)
	the_round.set_controllers(selection_1p, selection_2p, manual_controlled)
	queue_free()
