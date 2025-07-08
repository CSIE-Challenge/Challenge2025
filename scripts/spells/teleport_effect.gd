extends Area2D

var spell: TeleportSpell
var collision: CollisionShape2D
var duration_timer: Timer


func _ready():
	spell = get_parent()
	collision = $CollisionShape2D
	collision.shape.radius = spell.metadata.stats.radius
	clear_enemies()
	# Create duration timer
	duration_timer = Timer.new()
	duration_timer.one_shot = true
	duration_timer.timeout.connect(_on_duration_ended)
	add_child(duration_timer)
	duration_timer.wait_time = spell.metadata.stats.duration
	duration_timer.start()


func _draw():
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color.BLUE)


func clear_enemies() -> void:
	var enemies = get_enemies()
	for enemy in enemies:
		enemy.transport()


func get_enemies() -> Array[Node]:
	var entities = get_overlapping_bodies()
	print(entities)
	var enemies: Array[Node] = []

	for entity in entities:
		if entity.is_in_group("enemies"):
			enemies.append(entity)

	return enemies


func _on_body_entered(body):
	if body.is_in_group("enemies"):
		body.transport()


func _on_duration_ended():
	queue_free()
