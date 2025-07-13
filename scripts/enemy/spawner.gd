class_name Spawner
extends Node

signal spawn_enemy(unit_data: Dictionary)

@export var delay_between_waves: float = 5.0
@export var wave_info_label: Label

var wave_spawn_timer: Timer
var next_wave_timer: Timer

var wave_data := EnemyData.new()

var current_wave_index: int = -1
var current_wave_data: Dictionary
var unit_queue: Array = []


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


func _ready():
	wave_spawn_timer = Timer.new()
	add_child(wave_spawn_timer)
	wave_spawn_timer.connect("timeout", _on_wave_spawn_timer_timeout)

	next_wave_timer = Timer.new()
	add_child(next_wave_timer)
	next_wave_timer.connect("timeout", _on_next_wave_timer_timeout)

	start_next_wave()


func _process(_delta: float):
	wave_info_label.text = _get_wave_info()


func _get_wave_info() -> String:
	var time_left = next_wave_timer.time_left
	var seconds = int(time_left) % 60
	var milliseconds = int((time_left - int(time_left)) * 10)
	return "Wave %d         %02d.%1d" % [current_wave_data.wave_number, seconds, milliseconds]


func _prepare_unit_queue():
	unit_queue.clear()

	if current_wave_data.method == "sequential":
		for unit in current_wave_data.units:
			for i in range(unit.count):
				unit_queue.append(unit.name)

	elif current_wave_data.method == "random":
		for unit in current_wave_data.units:
			for i in range(unit.count):
				unit_queue.append(unit.name)
		unit_queue.shuffle()

	elif current_wave_data.method == "alternating":
		var units = current_wave_data.units.duplicate()
		while units.size() > 0:
			var unit = units.pop_front()
			unit_queue.append(unit.name)
			unit.count -= 1
			if unit.count > 0:
				units.append(unit)


func start_next_wave():
	current_wave_index += 1

	if current_wave_index >= wave_data.wave_data_list.size():
		printerr("All waves completed ?!")
		return

	current_wave_data = wave_data.wave_data_list[current_wave_index]

	# print("Starting Wave ", current_wave_data.wave_number)

	_prepare_unit_queue()
	# print("Unit queue prepared: ", unit_queue)

	wave_spawn_timer.wait_time = current_wave_data.delay
	wave_spawn_timer.start()

	next_wave_timer.wait_time = unit_queue.size() * current_wave_data.delay + delay_between_waves
	next_wave_timer.one_shot = true
	next_wave_timer.start()


func _on_wave_spawn_timer_timeout():
	# spawn a unit from the queue
	var unit_name = unit_queue.pop_front()

	var unit_data = wave_data.unit_data_list[unit_name]
	# print("Spawning unit: ", unit_data)
	spawn_enemy.emit(unit_data)

	if unit_queue.size() == 0:
		wave_spawn_timer.stop()


func _on_next_wave_timer_timeout():
	start_next_wave()
