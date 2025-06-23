extends CharacterBody2D

@export var speed := 300.0
@export var max_health := 100

var path_follow: PathFollow2D
var health: int

@onready var health_bar := $HealthBar


func _ready():
	path_follow = get_parent() as PathFollow2D
	health = max_health


func _process(delta):
	path_follow.progress += speed * delta
	if path_follow.progress_ratio >= 1.0:
		queue_free()

	health_bar.rotation = -path_follow.rotation
	health_bar.value = health / float(max_health) * 100.0


func take_damage(amount: int):
	health -= amount
	if health <= 0:
		die()


func die():
	queue_free()
