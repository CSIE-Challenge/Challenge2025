class_name ShopItem
extends AspectRatioContainer

var callback: Callable = func(): print("yay")
var display_scene: PackedScene
var display_cost: int = 10
var display_name: String = ""


func _ready():
	$TextureButton.pressed.connect(_on_button_press)
	$CenterContainer/Control.add_child(display_scene.instantiate())
	if display_cost > 0:
		$Cost.text = "$%d" % display_cost
	else:
		$Cost.text = ""
	if not display_name.is_empty():
		$Name.text = display_name


func _process(_delta):
	# Shouldn't be a performance issue here...
	custom_minimum_size = Vector2(size.x, size.x)


func _on_button_press() -> void:
	callback.call()
