class_name RangeIndicator
extends Node2D
var spell


func _ready():
	spell = get_parent()


func _draw():
	# Your drawing code goes here
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color.GREEN)
