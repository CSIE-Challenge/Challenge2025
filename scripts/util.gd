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
