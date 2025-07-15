extends Map

# 10% trigger chance
@onready var creature_clicked = randf() >= 0.5


func _on_game_manual_control_changed(value):
	$Creature.visible = value and (!creature_clicked)


func _ready() -> void:
	_on_game_manual_control_changed(self.game.is_manually_controlled)
	game.on_manual_control_changed.connect(_on_game_manual_control_changed)


func _on_input_event(_viewport, event: InputEvent, _shape_idx) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		creature_clicked = true
		_on_game_manual_control_changed(self.game.is_manually_controlled)

		var secret_scene = load("res://scenes/maps/water/egg-hint.tscn").instantiate()
		get_tree().get_root().add_child(secret_scene)
