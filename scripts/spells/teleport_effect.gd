extends Area2D
@onready var game: Game = get_node("../../../")
@onready var spell: TeleportSpell = get_parent()
@onready var collision: CollisionShape2D = $CollisionShape2D
@onready var duration_timer: Timer = $DurationTimer


func _ready():
	spell = get_parent()
	collision = $CollisionShape2D
	collision.shape.radius = spell.metadata.stats.radius
	# Create duration timer
	duration_timer.timeout.connect(_on_duration_ended)
	duration_timer.wait_time = spell.metadata.stats.duration
	duration_timer.start()
	# Create trigger timer
	# trigger_timer.timeout.connect(_on_trigger)
	# trigger_timer.wait_time = spell.metadata.stats.trigger_interval


func _draw():
	draw_circle(Vector2.ZERO, spell.metadata.stats.radius, Color(0.1, 0.8, 0.3, 0.4))


func trigger() -> void:
	var enemies: Array[Area2D] = get_overlapping_areas()
	for enemy: Enemy in enemies:
		if not enemy is Enemy:
			return
		enemy.transport()


func _physics_process(_delta: float) -> void:
	trigger()


func _on_duration_ended():
	queue_free()
