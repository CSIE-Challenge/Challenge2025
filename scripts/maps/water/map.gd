extends Map

var cells = [Vector2i(8, 8), Vector2i(9, 8), Vector2i(7, 9), Vector2i(8, 9), Vector2i(9, 9)]
var on_whale = 0

# 50% trigger chance
@onready var creature_clicked = randf() >= 0.5
@onready var splash_animation_timer = $SplashAnimation
@onready var splash_effect_timer = $SplashEffect


func _on_game_manual_control_changed(value):
	$Creature.visible = value and (!creature_clicked)


func _ready() -> void:
	_on_game_manual_control_changed(self.game.is_manually_controlled)
	game.on_manual_control_changed.connect(_on_game_manual_control_changed)
	game.tower_placed.connect(_on_tower_placed)
	game.tower_demolished.connect(_on_tower_demolished)
	splash_animation_timer.timeout.connect(
		func():
			$Splash.play()
			splash_effect_timer.start()
	)
	splash_effect_timer.timeout.connect(
		func():
			for pos in cells:
				game.demolish_tower.emit(pos)
	)


func _on_tower_placed(pos: Vector2i):
	on_whale += cells.count(pos)
	if on_whale > 0 and splash_animation_timer.is_stopped():
		splash_animation_timer.start()


func _on_tower_demolished(pos: Vector2i):
	on_whale -= cells.count(pos)
	if on_whale == 0:
		splash_animation_timer.stop()


func _on_input_event(_viewport, event: InputEvent, _shape_idx) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		creature_clicked = true
		_on_game_manual_control_changed(self.game.is_manually_controlled)

		var secret_scene = load("res://scenes/maps/water/egg-hint.tscn").instantiate()
		get_tree().get_root().add_child(secret_scene)
