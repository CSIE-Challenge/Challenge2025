extends TextureRect

# gdlint: disable=duplicated-load
const SHOP_ITEM_SCENE := preload("res://scenes/ui/shop_item.tscn")

@export var options_container: VBoxContainer
var building_game: Game
var opposing_game: Game


func start_game(_building_game: Game, _opposing_game: Game) -> void:
	building_game = _building_game
	opposing_game = _opposing_game


func _ready() -> void:
	_create_tower_options()
	_create_unit_options()
	_create_spell_options()


func _create_section(title: String) -> GridContainer:
	var tower_submenu := VBoxContainer.new()
	var tower_label := Label.new()
	var tower_grid := GridContainer.new()
	tower_submenu.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tower_grid.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tower_label.text = title
	tower_grid.columns = 3
	tower_grid.add_theme_constant_override("h_separation", 16)
	tower_grid.add_theme_constant_override("v_separation", 16)
	tower_submenu.add_theme_constant_override("separation", 8)
	tower_submenu.add_child(tower_label)
	tower_submenu.add_child(tower_grid)
	options_container.add_child(tower_submenu)
	return tower_grid


func _create_tower_options() -> void:
	var tower_data = TowerData.new()
	var grid := _create_section("Towers")
	for tower in tower_data.tower_data_list:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		var scene = load(tower)
		shop_item.callback = func(): building_game.buy_tower.emit(scene)
		shop_item.display_scene = scene
		var inst = scene.instantiate()
		shop_item.display_cost = inst.building_cost
		var ab: String
		if inst.level_a == inst.level_b:
			ab = ""
		else:
			ab = "a" if inst.level_a > inst.level_b else "b"
		shop_item.display_name = ("lv. %d%s" % [max(inst.level_a, inst.level_b), ab])
		inst.queue_free()
		grid.add_child(shop_item)


func _create_unit_options() -> void:
	var unit_data = EnemyData.new()
	var grid := _create_section("Units")
	for unit in unit_data.unit_data_list:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		var data = unit_data.unit_data_list[unit]
		var scene = load(data.get("scene_path"))
		shop_item.callback = func():
			if (
				(not opposing_game.enemy_cooldown.has(int(data.stats.type)))
				and building_game.spend(data.stats.deploy_cost, data.stats.income_impact)
			):
				opposing_game.summon_enemy.emit(data)
		shop_item.display_cost = data.stats.deploy_cost
		shop_item.display_scene = scene
		grid.add_child(shop_item)


func _create_spell_options() -> void:
	var grid := _create_section("Spells")
	for spell in [PoisonSpell, DoubleIncomeSpell, TeleportSpell]:
		var shop_item := SHOP_ITEM_SCENE.instantiate()
		shop_item.callback = func(): building_game.buy_spell.emit(spell)
		shop_item.display_cost = 0
		shop_item.display_scene = load(spell.metadata["scene_path"])
		grid.add_child(shop_item)


func _on_switch_pressed() -> void:
	self.visible = false
