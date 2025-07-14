extends Control

const CONFIG_FILE_PATH = "user://player_settings.cfg"

# array of: map name, cover image, scene
# the random option MUST be the first one
const MAP_LIST = [
	["隨機", preload("res://assets/background_image/random_map.png"), null],
	["地圖一", preload("res://assets/maps/Map1.png"), preload("res://scenes/maps/map1.tscn")],
	["小村探秘", preload("res://assets/maps/Map2.png"), preload("res://scenes/maps/map2.tscn")],
	["椰林大道", preload("res://assets/maps/Map3.png"), preload("res://scenes/maps/map3.tscn")],
	[" ", preload("res://assets/maps/space/preview.png"), preload("res://scenes/maps/space.tscn")]
]

var selected_map_idx: int

@onready var selection_1p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection1P
@onready var selection_2p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection2P
@onready var map_panel = $VBoxContainer/HBoxContainer/PanelMap


func _ready() -> void:
	selection_1p.manual_control_enabled.connect(func(): selection_2p.manual_control = false)
	selection_2p.manual_control_enabled.connect(func(): selection_1p.manual_control = false)
	map_panel.get_node(^"HBoxContainer/TextureButtonLeft").pressed.connect(
		func(): _select_map(selected_map_idx - 1)
	)
	map_panel.get_node(^"HBoxContainer/TextureButtonRight").pressed.connect(
		func(): _select_map(selected_map_idx + 1)
	)

	_load_config()
	_select_map(selected_map_idx)

	if selection_1p.manual_control and selection_2p.manual_control:
		selection_2p.manual_control = false


func _load_config() -> void:
	var config = ConfigFile.new()
	if config.load(CONFIG_FILE_PATH) != OK:
		selected_map_idx = 1
		config = ConfigFile.new()
		selection_1p.load_config(config, "Player 1")
		selection_2p.load_config(config, "Player 2")
		return
	selected_map_idx = config.get_value("Map", "index", 1)
	selection_1p.load_config(config, "Player 1")
	selection_2p.load_config(config, "Player 2")


func _save_config() -> void:
	var config = ConfigFile.new()
	config.set_value("Map", "index", selected_map_idx)
	selection_1p.save_config(config, "Player 1")
	selection_2p.save_config(config, "Player 2")
	config.save(CONFIG_FILE_PATH)


func _select_map(new_map_idx: int) -> void:
	var num_maps = len(MAP_LIST)
	selected_map_idx = (new_map_idx % num_maps + num_maps) % num_maps
	var map_info = MAP_LIST[selected_map_idx]
	map_panel.get_node(^"HBoxContainer/Label").text = map_info[0]
	map_panel.get_node(^"Panel/TextureRect").texture = map_info[1]


func _on_start_button_pressed() -> void:
	selection_1p.freeze()
	selection_2p.freeze()
	_save_config()

	AudioManager.button_on_click.play()
	AudioManager.background_menu.stop()

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

	# transfer node, so the python process is kept (and therefore, freed after the game ends)
	selection_1p.python_subprocess.reparent(the_round)
	selection_2p.python_subprocess.reparent(the_round)
	queue_free()


func _on_back_button_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/menu.tscn")
