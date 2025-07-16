extends Control

var the_rounds: Array[Round]

@onready var subviewports: Array[SubViewport] = [
	$SubViewportContainerNw/SubViewport,
	$SubViewportContainerNe/SubViewport,
	$SubViewportContainerSw/SubViewport,
	$SubViewportContainerSe/SubViewport,
]


func set_rounds(_the_rounds: Array[Round]) -> void:
	the_rounds = _the_rounds


func _ready() -> void:
	for i in range(4):
		subviewports[i].add_child(the_rounds[i])
	add_child(preload("res://scenes/pause_menu.tscn").instantiate())
