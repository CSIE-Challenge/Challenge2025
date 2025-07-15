class_name RangeIndicator
extends Node2D
var spell


func _ready():
	spell = get_parent()


func _draw():
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color.WHITE)
