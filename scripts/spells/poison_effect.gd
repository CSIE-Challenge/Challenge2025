extends Area2D
@onready var game: Game = get_node("../../../")
@onready var spell: PoisonSpell = get_parent()
@onready var collision: CollisionShape2D = $CollisionShape2D
@onready var duration_timer: Timer = $DurationTimer


func _ready():
	collision.shape.radius = spell.metadata.stats.radius
	# Create duration timer
	duration_timer.timeout.connect(_on_duration_ended)
	duration_timer.wait_time = spell.metadata.stats.trigger_interval * 1.1
	duration_timer.start()


func _draw():
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color(0.4, 0.2, 0.8, 0.4))


func _on_duration_ended():
	queue_free()


func _on_area_entered(area: Area2D) -> void:
	if area.is_in_group("enemies"):
		area.take_damage(spell.metadata.stats.trigger_damage)
