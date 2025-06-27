class_name Game
extends Node2D

const TOWER_COST = 5
const SKILL_SLOW = 0
const SKILL_AOE = 1

@export var tower_scene: PackedScene

var preview_tower
var money: int = 0
var money_per_second: int = 10
var max_hp: int = 100
var cost: int = 30
var cooldown: Array = [0.0, 0.0]

var cell_to_tower: Dictionary = {}

var _money_timer := 0.0

@onready var money_label: Label = $CanvasLayer/money_display
@onready var upgrade_button: Button = $CanvasLayer/upgrade

@onready var tilemap: TileMapLayer = $TileMapLayer
@onready var towers_node: Node2D = $Towers

@onready var hp_bar = $CanvasLayer/HitPoint
@onready var attack_ui: Control = $CanvasLayer/Attack

@onready var slow_button: Button = $CanvasLayer/skill_slow
@onready var aoe_button: Button = $CanvasLayer/aoe_damage

@onready var tower_ui := $CanvasLayer2/TowerUI


func _ready():
	preview_tower = tower_scene.instantiate()
	preview_tower.is_preview = true
	add_child(preview_tower)

	hp_bar.max_value = max_hp
	hp_bar.value = max_hp
	tower_ui.game = self


func _process(_delta):
	var mouse_pos = get_global_mouse_position()
	var cell = tilemap.local_to_map(tilemap.to_local(mouse_pos))
	var world_pos = tilemap.map_to_local(cell)

	if not tower_ui.visible:
		preview_tower.global_position = tilemap.to_global(world_pos)
		preview_tower.visible = _handle_visibility_of_preview_tower()

		var valid = can_place_tower(cell)
		set_tower_color(preview_tower, valid)

	upgrade_button.text = "cost $%d to upgrade" % cost
	money_label.text = "Money  :  $ " + str(money)
	_money_timer += _delta
	if _money_timer > 1.0:
		money += money_per_second
		_money_timer = 0.0

	slow_button.text = (
		"slow down enemies (CD: %.2f)"
		% maxf(0.0, cooldown[SKILL_SLOW] - Time.get_unix_time_from_system())
	)
	aoe_button.text = (
		"damage on fastest 5 enemies (CD: %.2f)"
		% maxf(0.0, cooldown[SKILL_AOE] - Time.get_unix_time_from_system())
	)


func set_tower_color(tower: Node2D, is_valid: bool):
	var color = Color(0, 1, 0, 0.5) if is_valid else Color(1, 0, 0, 0.5)
	for child in tower.get_children():
		if child is CanvasItem:
			child.modulate = color


func _unhandled_input(event: InputEvent):
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var cell = tilemap.local_to_map(tilemap.to_local(get_global_mouse_position()))
		if can_place_tower(cell):
			place_tower(cell)

	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_RIGHT:
		var cell = tilemap.local_to_map(tilemap.to_local(get_global_mouse_position()))
		var tower: Tower = cell_to_tower.get(cell, null)
		if tower == null:
			return

		var upgrade_cost: int = tower.level * 10
		if money >= upgrade_cost:
			money -= upgrade_cost
			tower.upgrade()


func can_place_tower(cell: Vector2i) -> bool:
	var tile_data = tilemap.get_cell_tile_data(cell)
	if tile_data == null:
		return false

	if money < TOWER_COST:
		return false

	if cell_to_tower.has(cell):
		return false

	return tile_data.get_custom_data("buildable") == true


func place_tower(cell: Vector2i):
	money -= TOWER_COST
	var tower = tower_scene.instantiate()
	var world_pos = tilemap.map_to_local(cell)
	tower.global_position = tilemap.to_global(world_pos)
	tower.connect("tower_selected", self._on_tower_selected)
	towers_node.add_child(tower)
	cell_to_tower[cell] = tower


func upgrade_income() -> void:
	if money >= cost:
		money_per_second += 1
		money -= cost
		cost += 30


func _on_upgrade_pressed() -> void:
	upgrade_income()


func set_hit_point(damage: int):
	hp_bar.value -= damage


func _handle_visibility_of_preview_tower():
	if (
		attack_ui.panel.visible
		and attack_ui.panel.get_global_rect().has_point(get_global_mouse_position())
	):
		return false
	if (
		attack_ui.open_button.visible
		and attack_ui.open_button.get_global_rect().has_point(get_global_mouse_position())
	):
		return false
	if (
		upgrade_button.visible
		and upgrade_button.get_global_rect().has_point(get_global_mouse_position())
	):
		return false

	# Not visible if money is not enough
	if money < TOWER_COST:
		return false
	return true


func start_cooldown(skill: int, cd: float):
	cooldown[skill] = Time.get_unix_time_from_system() + cd


func is_on_cooldown(skill: int) -> bool:
	return cooldown[skill] > Time.get_unix_time_from_system()


func slow_down_enemy():
	var skill_cost: int = 50
	var cd: float = 15.0
	if money < skill_cost or is_on_cooldown(SKILL_SLOW):
		print("fail")
		return

	money -= skill_cost
	start_cooldown(SKILL_SLOW, cd)
	for enemy in get_tree().get_nodes_in_group("enemies"):
		enemy.slow_down()


func _on_skill_slow_pressed() -> void:
	slow_down_enemy()


func aoe_damage():
	var skill_cost: int = 100
	var cd: float = 60.0
	if money < skill_cost or is_on_cooldown(SKILL_AOE):
		print("fail")
		return

	money -= skill_cost
	start_cooldown(SKILL_AOE, cd)
	var enemies := get_tree().get_nodes_in_group("enemies")
	print(enemies.size())
	enemies.sort_custom(
		func(a, b): return a.path_follow.progress_ratio > b.path_follow.progress_ratio
	)
	for i in range(min(enemies.size(), 5)):
		enemies[i].take_damage(50)


func _on_aoe_damage_pressed() -> void:
	aoe_damage()


func _on_tower_selected(tower):
	tower_ui.global_position = tower.global_position
	tower_ui.selected_tower = tower
	tower_ui.visible = true
