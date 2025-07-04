extends TabBar

# gdlint: disable=duplicated-load
# temporarily disable for testing purposes
const TOWER_SCENES := [
	preload("res://scenes/towers/twin_turret.tscn"),
	preload("res://scenes/towers/twin_turret.tscn"),
	preload("res://scenes/towers/twin_turret.tscn"),
	preload("res://scenes/towers/twin_turret.tscn")
]
const SHOP_ITEM_SCENE := preload("res://scenes/ui/shop_item.tscn")

@export var options_container: VBoxContainer
@export var building_game: Game


func _ready() -> void:
	_create_tower_options()


func _create_section(title: String) -> GridContainer:
	var tower_submenu := VBoxContainer.new()
	var tower_label := Label.new()
	var tower_grid := GridContainer.new()
	tower_label.text = title
	tower_grid.columns = 3
	tower_grid.add_theme_constant_override("h_separation", 16)
	tower_grid.add_theme_constant_override("v_separation", 16)
	tower_submenu.add_child(tower_label)
	tower_submenu.add_child(tower_grid)
	options_container.add_child(tower_submenu)
	return tower_grid


func _create_tower_options() -> void:
	var grid := _create_section("Towers")
	for scene in TOWER_SCENES:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		shop_item.callback = func(): building_game.buy_tower.emit(scene)
		grid.add_child(shop_item)
		print("what")
