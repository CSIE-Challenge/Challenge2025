class_name Enemy
extends CharacterBody2D

signal killed()
signal reached()

@export var speed := 300.0
@export var max_health := 100

var path_follow: PathFollow2D
var health: int
var damage: int = 5
var speed_scale: float = 1.0
var slow_timer := Timer.new()
var source: Game.EnemySource

@onready var health_bar := $HealthBar


# _init not overridden because PackedScene.instantiate() does not accept arguments
func init(_source: Game.EnemySource) -> void:
	source = _source
	path_follow = PathFollow2D.new()
	path_follow.loop = false
	path_follow.add_child(self)


func _ready():
	health = max_health
	path_follow.progress_ratio = 0
	add_to_group("enemies")
	slow_timer.one_shot = true
	slow_timer.connect("timeout", Callable(self, "_on_slow_timeout"))
	add_child(slow_timer)


func _process(delta):
	path_follow.progress += speed * delta * speed_scale
	if path_follow.progress_ratio >= 0.99:
		reached.emit()

	health_bar.rotation = -path_follow.rotation
	health_bar.value = health / float(max_health) * 100.0


func _exit_tree() -> void:
	path_follow.queue_free()


func take_damage(amount: int):
	health -= amount
	if health <= 0:
		killed.emit()


func slow_down():
	speed_scale = 0.5
	slow_timer.start(5.0)


func _on_slow_timeout():
	speed_scale = 1.0
