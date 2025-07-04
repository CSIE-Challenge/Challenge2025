extends AspectRatioContainer


func _ready():
	await get_tree().process_frame
	custom_minimum_size = Vector2(size.x, size.x)
