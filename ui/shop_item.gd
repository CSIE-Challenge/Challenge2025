class_name ShopItem
extends AspectRatioContainer

@export var callback: Callable


func _ready():
	await get_tree().process_frame
	custom_minimum_size = Vector2(size.x, size.x)
	self.gui_input.connect(_on_gui_input)


func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		callback.call()
