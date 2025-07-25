extends Sprite2D

const LAYER_9_BIT = 1 << 8

@export var map: Control
@export var speed = 150.0
var end: float

@onready var boom_scene = preload("res://scenes/maps/boom.tscn")


func _process(delta: float) -> void:
	position.x += speed * delta
	if position.x > end and visible:
		visible = false
		explode()


func explode():
	var enemies: Array[Area2D] = $Area2D.get_overlapping_areas()

	for e in enemies:
		if e.collision_layer & LAYER_9_BIT != 0:
			var cell_pos = map.global_to_cell(e.global_position)
			map.game.demolish_tower.emit(cell_pos)
		elif e.has_method("take_damage"):
			e.take_damage(1000000)

	for i in range(10):
		var boom = boom_scene.instantiate()
		boom.position = position + Vector2(randf_range(-120, 120), randf_range(-120, 120))
		map.add_child(boom)
