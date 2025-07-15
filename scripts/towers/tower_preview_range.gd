class_name TowerPreviewRange
extends Node2D

var color: Color = Color(1, 1, 1, 0.2)
var _radius: float


func _init(radius: float) -> void:
	_radius = radius


func _draw():
	draw_circle(Vector2(0, 0), _radius, color)
