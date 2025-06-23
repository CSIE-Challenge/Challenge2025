extends StaticBody2D

var damage: int = 10
var speed: float = 400  # per second
var direction: Vector2 = Vector2(0, 1)


func _ready() -> void:
	pass


func _process(delta: float) -> void:
	pass


func _physics_process(delta: float) -> void:
	position += delta * speed * direction
