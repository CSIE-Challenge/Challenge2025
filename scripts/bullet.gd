extends StaticBody2D

var damage: int = 10
var speed: float = 600  # per second
var direction: Vector2 = Vector2(0, 1)


func _ready() -> void:
	direction = Vector2(cos(rotation - PI / 2), sin(rotation - PI / 2))


func _process(delta: float) -> void:
	pass


func _physics_process(delta: float) -> void:
	position += delta * speed * direction
