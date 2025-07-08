extends Node2D


func _ready():
	# hide the spell
	for child in get_children():
		child.get_node("Sprite2D").hide()
