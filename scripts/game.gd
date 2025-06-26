extends Node2D

const TOWER_COST = 5

@export var tower_scene: PackedScene

var occupied_cells := {}
var preview_tower
var money: int = 0
var money_per_second: int = 10
var max_hp: int = 100
var cost = 30
var _money_timer := 0.0

@onready var money_label: Label = $CanvasLayer/money_display
@onready var upgrade_button: Button = $CanvasLayer/upgrade

@onready var tilemap: TileMapLayer = $TileMapLayer
@onready var towers_node: Node2D = $Towers

@onready var hp_bar = $HitPoint
@onready var attack_ui: Control = $Attack

@onready var tower_ui := $CanvasLayer2/TowerUI


func _ready():
	preview_tower = tower_scene.instantiate()
	preview_tower.is_preview = true
	add_child(preview_tower)

	hp_bar.max_value = max_hp
	hp_bar.value = max_hp


func _process(_delta):
	var mouse_pos = get_global_mouse_position()
	var cell = tilemap.local_to_map(tilemap.to_local(mouse_pos))
	var world_pos = tilemap.map_to_local(cell)

	preview_tower.global_position = tilemap.to_global(world_pos)
	preview_tower.visible = handle_visibility_of_preview_tower()

	var valid = can_place_tower(cell)
	set_tower_color(preview_tower, valid)

	upgrade_button.text = "cost $%d to upgrade" % cost
	money_label.text = "Money  :  $ " + str(money)
	_money_timer += _delta
	if _money_timer > 1.0:
		money += money_per_second
		_money_timer = 0.0


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


func can_place_tower(cell: Vector2i) -> bool:
	var tile_data = tilemap.get_cell_tile_data(cell)
	if tile_data == null:
		return false

	if money < TOWER_COST:
		return false

	if occupied_cells.has(cell):
		return false

	return tile_data.get_custom_data("buildable") == true


func place_tower(cell: Vector2i):
	money -= TOWER_COST
	var tower = tower_scene.instantiate()
	var world_pos = tilemap.map_to_local(cell)
	tower.global_position = tilemap.to_global(world_pos)
	tower.connect("tower_selected", self._on_tower_selected)
	occupied_cells[cell] = true
	towers_node.add_child(tower)


func upgrade_income() -> void:
	if money >= cost:
		money_per_second += 1
		money -= cost
		cost += 30


func _on_upgrade_pressed() -> void:
	upgrade_income()


func set_hit_point(damage: int):
	hp_bar.value -= damage


func handle_visibility_of_preview_tower():
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
	return true


func _on_tower_selected(tower):
	tower_ui.global_position = tower.global_position
	tower_ui.visible = true
