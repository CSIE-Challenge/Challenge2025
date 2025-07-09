extends Area2D
@onready var game: Game = get_node("../../../")
@onready var spell: PoisonSpell = get_parent()
@onready var collision: CollisionShape2D = $CollisionShape2D
@onready var duration_timer: Timer = $DurationTimer
@onready var trigger_timer: Timer = $TriggerTimer


func _ready():
	collision.shape.radius = spell.metadata.stats.radius
	# Create duration timer
	duration_timer.timeout.connect(_on_duration_ended)
	duration_timer.wait_time = spell.metadata.stats.duration
	# Create trigger timer
	trigger_timer.timeout.connect(_on_trigger)
	trigger_timer.wait_time = spell.metadata.stats.trigger_interval


func _draw():
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color.BLUE)


func trigger() -> void:
	var enemies: Array[Area2D] = get_overlapping_areas()
	for enemy in enemies:
		# TODO: replace with true poison logic
		enemy.transport()


func _on_trigger():
	trigger()


func _on_duration_ended():
	queue_free()
