class_name Util

##### This part is for layer #####
### All UI layer should be above 150 ###
# pause_menu: 200
# shop_item: 160, with items above higher (relative z_index)
# menu: 150
# tower_ui: 150
### End of UI ###

const BULLET_LAYER = 90  # The default layer of bullet
const FLYING_LAYER = 70
# Default tower and enemy have the layer of 60.
# Note that the health bar is 50 layers above the enemy itself,
# ensuring that it is above the towers.
# Therefore, the (relative) z_index of enemy health bar should be changed when changing TOWER_LAYER
const TOWER_LAYER = 50
const ENEMY_LAYER = 50
const EFFECT_LAYER = 40  # Should be above the top path but under the top enemies

# The following constant are defined for space
const TERRAIN = 35
const H_PATH = 30
const M_ENEMY = 25
const M_PATH = 20
const L_ENEMY = 15
const L_PATH = 10
##### End of layer #####


static func load_json(file_path: String):
	var file = FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		push_error(
			"[Util] Failed to open file: %s, reason: %d" % [file_path, FileAccess.get_open_error()]
		)
		return null

	var content = file.get_as_text()
	file.close()

	var json_parsed = JSON.parse_string(content)
	if json_parsed == null:
		push_error("[Util] Failed to parse JSON from file: ", file_path)
		return null

	return json_parsed


static func save_json(file_path: String, data: Variant) -> void:
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file == null:
		push_error(
			"[Util] Failed to open file: %s, reason: %d" % [file_path, FileAccess.get_open_error()]
		)
		return

	var dumped = JSON.stringify(data, "  ")
	if not file.store_string(dumped):
		push_error("[Util] Failed to write data to file: ", file_path)
	file.close()


static func get_string_width(node: Control, content: String) -> float:
	return (
		node
		. get_theme_default_font()
		. get_string_size(
			content, HORIZONTAL_ALIGNMENT_LEFT, -1, node.get_theme_default_font_size()
		)
		. x
	)


static func truncate_front(node: Control, content: String, max_width: float) -> String:
	if get_string_width(node, content) < max_width:
		return content
	for i in range(len(content)):
		var truncated = "…" + content.substr(i)
		if get_string_width(node, truncated) < max_width:
			return truncated
	return ""
