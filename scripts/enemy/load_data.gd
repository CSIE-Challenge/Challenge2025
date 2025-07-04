class_name EnemyData

var wave_data_path: String = "res://data/waves.json"
var wave_data_list: Array

var unit_data_path: String = "res://data/units.json"
var unit_data_list: Dictionary


func load_json(file_path: String):
	var file = FileAccess.open(file_path, FileAccess.READ)
	if file == null:
		printerr("Failed to open file: ", file_path)
		return null

	var content = file.get_as_text()
	file.close()

	var json_parsed = JSON.parse_string(content)
	if json_parsed == null:
		printerr("Failed to parse JSON from file: ", file_path)
		return null

	return json_parsed


func _init():
	wave_data_list = load_json(wave_data_path)
	unit_data_list = load_json(unit_data_path)
