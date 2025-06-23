extends Area2D

var speed = 400
var damage
var target: Node2D = null
var direction: Vector2

func _ready() -> void:
	body_entered.connect(Callable(self, "_on_body_entered"))


func _process(delta: float) -> void:
	if target != null and target.is_inside_tree():
		var to_target = target.global_position - global_position
		rotation = to_target.angle()
		direction = Vector2.RIGHT.rotated(rotation)
	position += direction * speed * delta

	if position.x > get_viewport_rect().size.x or position.x < 0:
		print("Bullet out of bounds")
		queue_free()


func _on_body_entered(body: Node2D) -> void:
	body.take_damage(damage)
	print("Bullet Hit: ", body.name)
	queue_free()
