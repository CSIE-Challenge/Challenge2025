extends Control

const GAME_DURATION = 180.0

@export var game_timer_label: Label
@export var score_bar: ScoreBar


func _ready() -> void:
	$GameTimer.wait_time = GAME_DURATION
	$GameTimer.one_shot = true
	$GameTimer.start()


func get_formatted_time() -> String:
	var time_left = $GameTimer.time_left
	var minutes = int(time_left / 60)
	var seconds = int(time_left) % 60
	return "%02d:%02d" % [minutes, seconds]


func _update_score_bar() -> void:
	# TODO: actually calculate the score
	score_bar.left_score += randi_range(10, 100)
	score_bar.right_score += randi_range(10, 100)


func _process(_delta: float) -> void:
	game_timer_label.text = get_formatted_time()
	_update_score_bar()
