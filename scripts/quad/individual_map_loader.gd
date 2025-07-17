extends HBoxContainer

var map_scene: PackedScene


func _ready() -> void:
	visible = false


func init(match_options: Dictionary) -> void:
	var map_options = match_options["map"]
	$MapConfigContainer/MapNameContainer/MapName.text = map_options["name"]
	$MapPreviewContainer/MapPreview.texture = load(map_options["preview"])
	map_scene = load(map_options["scene-path"])
	$MapConfigContainer/TeamNameContainer/Left.text = match_options["player-left"]["name"]
	$MapConfigContainer/TeamNameContainer/Right.text = match_options["player-right"]["name"]
	visible = true


func reverse_horizontal() -> void:
	move_child(get_children()[1], 0)
