class_name ShopItem
extends AspectRatioContainer

var callback: Callable
var display_scene: PackedScene
var display_cost: int = 10
var display_name: String = ""


func _ready():
	self.gui_input.connect(_on_gui_input)
	$CenterContainer/Control.add_child(display_scene.instantiate())
	$Cost.text = "$%d" % display_cost
	if not display_name.is_empty():
		$Name.text = display_name


func _process(_delta):
	# Shouldn't be a performance issue here...
	custom_minimum_size = Vector2(size.x, size.x)


func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		callback.call()
