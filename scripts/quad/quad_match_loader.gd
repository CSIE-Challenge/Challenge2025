extends Control

# 1: config (first page)
# 2: connection panels (second page)
var active_section: int = 1

var match_config: Dictionary = {}
var config_path: String

@onready
var config_path_panel = $ConfigPanel/ConfigTextContainer/DefaultSettingsContainer/ConfigPathLabel
@onready var connection_panels = [
	[
		$ConnectionPanelContainer/Nw/Left,
		$ConnectionPanelContainer/Nw/Right,
	],
	[
		$ConnectionPanelContainer/Ne/Left,
		$ConnectionPanelContainer/Ne/Right,
	],
	[
		$ConnectionPanelContainer/Sw/Left,
		$ConnectionPanelContainer/Sw/Right,
	],
	[
		$ConnectionPanelContainer/Se/Left,
		$ConnectionPanelContainer/Se/Right,
	],
]
@onready var map_panels = [
	$ConfigPanel/ConfigTextContainer/MapConfigContainer/Nw,
	$ConfigPanel/ConfigTextContainer/MapConfigContainer/Ne,
	$ConfigPanel/ConfigTextContainer/MapConfigContainer/Sw,
	$ConfigPanel/ConfigTextContainer/MapConfigContainer/Se,
]


func load_config_file(_config_path: String) -> void:
	config_path = _config_path
	var data: Dictionary = Util.load_json(_config_path)
	match_config = data
	$TitleContainer/TitleLabel.text = data["title"]

	for i: int in range(4):
		var pos: String = ["nw", "ne", "sw", "se"][i]
		if not data.has(pos):
			continue
		var match_data = data[pos]
		map_panels[i].init(match_data)
		if i % 2 == 1:
			map_panels[i].reverse_horizontal()
		for j: int in range(2):
			var lr: String = ["player-left", "player-right"][j]
			connection_panels[i][j].init(match_data[lr], data["python-interpreter"])


func _gui_input(event: InputEvent) -> void:
	if (
		event is InputEventMouseButton
		and event.pressed
		and event.button_index == MOUSE_BUTTON_LEFT
		and config_path_panel.get_global_rect().has_point(event.position)
	):
		$ConfigPanel/ConfigTextContainer/DefaultSettingsContainer/ConfigSelection.popup()


func _on_config_selection_file_selected(path: String) -> void:
	load_config_file(path)
	# hard-code the width, otherwise getting the right width could be tricky
	config_path_panel.text = Util.truncate_front(self, path, 360)
	$ButtonsContainer/Next.disabled = false


func toggle_all_agents(run: bool) -> void:
	for i: int in range(4):
		for j: int in range(2):
			var subproc = connection_panels[i][j].selector.python_subprocess
			if run:
				subproc.run_subprocess()
				subproc.set_auto_restart(true)
			else:
				subproc.kill_subprocess()


func start_game() -> void:
	var the_rounds: Array[Round] = []
	for i in range(4):
		var map_scene = map_panels[i].map_scene
		var selection_1p = connection_panels[i][0].selector
		var selection_2p = connection_panels[i][1].selector
		var the_round = preload("res://scenes/round.tscn").instantiate()
		the_round.system_controlled = true
		the_round.set_controllers(selection_1p, selection_2p, 0)
		the_round.set_maps(map_scene)
		selection_1p.python_subprocess.reparent(the_round)
		selection_2p.python_subprocess.reparent(the_round)
		the_rounds.push_back(the_round)
	var the_quad = preload("res://scenes/quad/quad_match.tscn").instantiate()
	the_quad.init(config_path, match_config, the_rounds)
	get_tree().get_root().add_child(the_quad)
	queue_free()


func _on_next_button_pressed() -> void:
	match active_section:
		1:
			# proceed to connection panels
			active_section = 2
			$ButtonsContainer/Next.text = "Start"
			$ConfigPanel.visible = false
			$ConnectionPanelContainer.visible = true
			toggle_all_agents(true)
		2:
			# proceed to games
			AudioManager.button_on_click.play()
			AudioManager.background_menu.stop()
			start_game()


func _on_back_button_pressed() -> void:
	match active_section:
		1:
			# back to main screen
			get_tree().change_scene_to_file("res://scenes/menu.tscn")
		2:
			# back to match config
			active_section = 1
			$ButtonsContainer/Next.text = "Next"
			$ConfigPanel.visible = true
			$ConnectionPanelContainer.visible = false
			toggle_all_agents(false)
