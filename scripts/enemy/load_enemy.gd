class_name EnemyData

var wave_data_path: String = "res://data/waves.json"
var wave_data_list: Array

var unit_data_path: String = "res://data/units.json"
var unit_data_list: Dictionary


func _init():
	wave_data_list = Util.load_json(wave_data_path)
	unit_data_list = Util.load_json(unit_data_path)
