class_name Util


static func load_json(file_path: String):
	var file = FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		push_error("[Util] Failed to open file: ", file_path)
		return null

	var content = file.get_as_text()
	file.close()

	var json_parsed = JSON.parse_string(content)
	if json_parsed == null:
		push_error("[Util] Failed to parse JSON from file: ", file_path)
		return null

	return json_parsed


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
