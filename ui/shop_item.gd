class_name ShopItem
extends AspectRatioContainer

var callback: Callable
var display_scene: PackedScene
var display_cost: int = 10

@onready var container = $CenterContainer/Control


func _ready():
	await get_tree().process_frame
	custom_minimum_size = Vector2(size.x, size.x)
	self.gui_input.connect(_on_gui_input)
	$CenterContainer/Control.add_child(display_scene.instantiate())
	$Cost.text = "$%d" % display_cost


func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		callback.call()
