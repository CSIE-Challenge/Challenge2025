class_name TowerUi
extends Control

signal sold

var tower: Tower
var range_circle = null


func initialize(t: Tower):
	tower = t
	_draw_attack_range(tower.aim_range)


# the tower's UI intercepts input events before GUI (because it is impossible to trigger both)
func _input(event):
	if (
		event is InputEventMouseButton
		and event.button_index == MOUSE_BUTTON_LEFT
		and event.pressed
		and not get_global_rect().has_point(get_global_mouse_position())
	):
		queue_free()
		get_viewport().set_input_as_handled()


func _on_sell_button_pressed() -> void:
	sold.emit()


func _on_first_button_pressed() -> void:
	get_parent().strategy = Tower.TargetStrategy.FIRST
	queue_free()


func _on_close_button_pressed() -> void:
	get_parent().strategy = Tower.TargetStrategy.CLOSE
	queue_free()


func _on_last_button_pressed() -> void:
	get_parent().strategy = Tower.TargetStrategy.LAST
	queue_free()


func _create_range_circle(radius: float) -> Line2D:
	var circle := Line2D.new()
	circle.width = 5
	circle.default_color = Color(1, 1, 1, 0.3)
	circle.closed = true

	var segments := 64
	for i in segments:
		var angle = TAU * i / segments
		var point = Vector2(cos(angle), sin(angle)) * radius
		circle.add_point(point)
	return circle


func _draw_attack_range(radius: float) -> void:
	if range_circle:
		range_circle.queue_free()
	range_circle = _create_range_circle(radius)
	add_child(range_circle)
