class_name TowerPreviewRange
extends Node2D

var color: Color = Color(1, 1, 1, 0.2)
var _radius: float


func _init(radius: float) -> void:
	_radius = radius


func _draw():
	var corrected_radius = _radius / global_transform.get_scale().x
	draw_circle(Vector2(0, 0), corrected_radius, color)
