extends StaticBody2D

var is_preview := false

@onready var turret = $Turret


func _ready():
	if is_preview:
		apply_preview_appearance()


func apply_preview_appearance():
	for child in get_children():
		if child is CanvasItem:
			child.modulate = Color(1, 1, 1, 0.5)
	set_process(false)

# func _ready() -> void:
# 	pass

# func _process(delta: float) -> void:
# 	pass

# func _physics_process(delta: float) -> void:
# 	pass

# func aim(enemies) -> void:
# 	pass

# func shoot() -> void:
# 	pass
