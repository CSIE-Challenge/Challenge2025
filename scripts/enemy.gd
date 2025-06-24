extends CharacterBody2D

@export var speed := 300.0
@export var max_health := 100

var path_follow: PathFollow2D
var health: int
var damage: int = 5
var speed_scale: float = 1.0
var slow_timer := Timer.new()

@onready var health_bar := $HealthBar


func _ready():
	path_follow = get_parent() as PathFollow2D
	health = max_health

	add_to_group("enemies")
	slow_timer.one_shot = true
	slow_timer.connect("timeout", Callable(self, "_on_slow_timeout"))
	add_child(slow_timer)


func _process(delta):
	path_follow.progress += speed * delta * speed_scale
	if path_follow.progress_ratio >= 0.99:
		$"../../../".set_hit_point(damage)
		queue_free()

	health_bar.rotation = -path_follow.rotation
	health_bar.value = health / float(max_health) * 100.0


func take_damage(amount: int):
	health -= amount
	if health <= 0:
		die()


func die():
	queue_free()

func slow_down():
	speed_scale = 0.5
	slow_timer.start(5.0)

func _on_slow_timeout() :
	speed_scale = 1.0
