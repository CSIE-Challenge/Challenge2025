extends Control

# 1: config (first page)
# 2: connection panels (second page)
var active_section: int = 1
var map_scene: PackedScene

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


func load_config_file(config_path: String) -> void:
	var data: Dictionary = Util.load_json(config_path)
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
	config_path_panel.text = Util.truncate_front(self, path, config_path_panel.size.x)
	$ButtonsContainer/Next.disabled = false


func toggle_all_agents(run: bool) -> void:
	for i: int in range(4):
		for j: int in range(2):
			var subproc = connection_panels[i][j].selector.python_subprocess
			if run:
				subproc.run_subprocess()
				print(subproc._state, subproc.python_interpreter_path, subproc.python_script_path)
			else:
				subproc.kill_subprocess()


func start_game() -> void:
	pass


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
