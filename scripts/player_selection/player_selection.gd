extends Control

# array of: map name, cover image, scene
# the random option MUST be the first one
const MAP_LIST = [
	["Random", preload("res://assets/background_image/random_map.png"), null],
	["Map 1", preload("res://assets/maps/Map1.png"), preload("res://scenes/maps/map1.tscn")],
	["Map 2", preload("res://assets/maps/Map2.png"), preload("res://scenes/maps/map2.tscn")],
	["Map 3", preload("res://assets/maps/Map3.png"), preload("res://scenes/maps/map3.tscn")],
]

var selected_map_idx: int

@onready var selection_1p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection1P
@onready var selection_2p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection2P
@onready var game_start_button: Button = $VBoxContainer/StartButton
@onready var game_start_timer: Timer = $GameStartTimer
@onready var map_panel = $VBoxContainer/HBoxContainer/PanelMap


func _ready() -> void:
	selection_1p.manual_control_enabled.connect(func(): selection_2p.manual_control = false)
	selection_2p.manual_control_enabled.connect(func(): selection_1p.manual_control = false)
	selection_1p.manual_control = true
	map_panel.get_node(^"HBoxContainer/TextureButtonLeft").pressed.connect(
		func(): _select_map(selected_map_idx - 1)
	)
	map_panel.get_node(^"HBoxContainer/TextureButtonRight").pressed.connect(
		func(): _select_map(selected_map_idx + 1)
	)
	_select_map(1)


func _select_map(new_map_idx: int) -> void:
	selected_map_idx = (new_map_idx + len(MAP_LIST)) % len(MAP_LIST)
	var map_info = MAP_LIST[selected_map_idx]
	map_panel.get_node(^"HBoxContainer/Label").text = map_info[0]
	map_panel.get_node(^"Panel/TextureRect").texture = map_info[1]


func _on_start_button_pressed() -> void:
	if not game_start_timer.is_stopped():
		return
	selection_1p.freeze()
	selection_2p.freeze()
	game_start_button.text = "Starting..."
	game_start_timer.start()


func _on_game_start_timer_timeout() -> void:
	var manual_controlled = 0
	if selection_1p.manual_control:
		manual_controlled = 1
	if selection_2p.manual_control:
		manual_controlled = 2

	if selected_map_idx == 0:  # random
		selected_map_idx = randi_range(1, len(MAP_LIST) - 1)
	var map_scene = MAP_LIST[selected_map_idx][2]

	var the_round = preload("res://scenes/round.tscn").instantiate()
	the_round.set_controllers(selection_1p, selection_2p, manual_controlled)
	the_round.set_maps(map_scene)
	get_tree().get_root().add_child(the_round)
	queue_free()
