extends Control

# 1: config (first page)
# 2: connection panels (second page)
var active_section: int = 1
var map_scene: PackedScene

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


func _ready() -> void:
	load_config_file("res://data/quad-match.json")


func load_config_file(config_path: String) -> void:
	var data: Dictionary = Util.load_json(config_path)
	$TitleContainer/TitleLabel.text = data["title"]

	var map_data = data["map"]
	$ConfigContainer/ConfigPanel/ConfigTextContainer/MapNameContainer/LabelM.text = map_data["name"]
	$ConfigContainer/MapPreviewContainer/MapPreviewTexture.texture = load(map_data["preview"])
	map_scene = load(map_data["scene-path"])

	for i: int in range(4):
		for j: int in range(2):
			var pos: String = ["nw", "ne", "sw", "se"][i]
			var lr: String = ["player-left", "player-right"][j]
			connection_panels[i][j].init(data[pos][lr])
		var team_names_container = $ConfigContainer/ConfigPanel/ConfigTextContainer/TeamNamesContainer
		var team_names: Label = team_names_container.find_child(["Nw", "Ne", "Sw", "Se"][i])
		team_names.text = (
			"%s - %s"
			% [
				connection_panels[i][0].options["name"],
				connection_panels[i][1].options["name"],
			]
		)


func start_game() -> void:
	pass


func _on_next_button_pressed() -> void:
	match active_section:
		1:
			# back to match configs
			active_section = 2
			$ButtonsContainer/Next.text = "Start"
			$ConfigContainer.visible = false
			$ConnectionPanelContainer.visible = true
		2:
			# proceed to games
			start_game()


func _on_back_button_pressed() -> void:
	match active_section:
		1:
			# back to main screen
			get_tree().change_scene_to_file("res://scenes/menu.tscn")
		2:
			# proceed to connection panels
			active_section = 1
			$ButtonsContainer/Next.text = "Next"
			$ConfigContainer.visible = true
			$ConnectionPanelContainer.visible = false
