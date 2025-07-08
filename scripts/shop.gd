extends TabBar

# gdlint: disable=duplicated-load
# temporarily disable for testing purposes
const TOWER_SCENES := [
	preload("res://scenes/towers/donkey_kong_1.tscn"),
	preload("res://scenes/towers/fire_mario_1.tscn"),
	preload("res://scenes/towers/fort_1.tscn"),
	preload("res://scenes/towers/ice_luigi_1.tscn"),
	preload("res://scenes/towers/shy_guy_1.tscn")
]
const SHOP_ITEM_SCENE := preload("res://scenes/ui/shop_item.tscn")

@export var options_container: VBoxContainer
@export var building_game: Game
@export var opposing_game: Game


func _ready() -> void:
	_create_tower_options()
	_create_unit_options()
	_create_spell_options()


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
		shop_item.display_scene = scene
		shop_item.display_cost = scene.instantiate().building_cost
		grid.add_child(shop_item)


func _create_unit_options() -> void:
	var unit_data = EnemyData.new()
	var grid := _create_section("Units")
	for unit in unit_data.unit_data_list:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		var data = unit_data.unit_data_list[unit]
		var scene = load(data.get("scene_path"))
		shop_item.callback = func():
			if building_game.spend(data.stats.deploy_cost):
				opposing_game.summon_enemy.emit(data)
		shop_item.display_cost = data.stats.deploy_cost
		shop_item.display_scene = scene
		grid.add_child(shop_item)


func _create_spell_options() -> void:
	var grid := _create_section("Spells")
	for spell in [PoisonSpell, DoubleIncomeSpell, TeleportSpell]:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		shop_item.callback = func(): building_game.deploy_spell.emit(spell)
		shop_item.display_cost = spell.metadata["stats"]["cost"]
		shop_item.display_scene = load(spell.metadata["scene_path"])
		grid.add_child(shop_item)
