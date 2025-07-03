extends Control

const GAME_DURATION = 180.0

@onready var game_timer_label := $Screen/Bottom/Mid/GameStatus/VBoxContainer/Countdown


func _ready() -> void:
	$GameTimer.wait_time = GAME_DURATION
	$GameTimer.one_shot = true
	$GameTimer.start()


func get_formatted_time() -> String:
	var time_left = $GameTimer.time_left
	var minutes = int(time_left / 60)
	var seconds = int(time_left) % 60
	return "%02d:%02d" % [minutes, seconds]


func _process(_delta: float) -> void:
	game_timer_label.text = get_formatted_time()
