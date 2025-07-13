class_name TowerData

var tower_data_path: String = "res://data/towers.json"
var tower_data_list: Array
var util = Util.new()


func _init():
	tower_data_list = util.load_json(tower_data_path)
