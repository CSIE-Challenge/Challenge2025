extends Node2D

const TOWER_COST = 5
const SKILL_SLOW = 0
const SKILL_AOE = 1

@export var tower_scene: PackedScene
@export var is_ai: bool

var occupied_cells := {}
var preview_tower
var money: int = 0
var money_per_second: int = 10
var max_hp: int = 100
var cost: int = 30
var cooldown: Array = [0.0, 0.0]

var enemy_list = {
	"plane":
	{
		icon_path =
		"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile270.png",
		cost = 100,
		income = 1
	},
	"tank":
	{
		icon_path =
		"res://assets/kenney_tower-defense-top-down/PNG/Retina/towerDefense_tile204.png",
		cost = 200,
		income = 5
	},
	"robot":
	{
		icon_path =
		"res://.godot/imported/towerDefense_tile245.png-a634484bb16333c0b20a93f4d77d94ba.ctex",
		cost = 300,
		income = 10
	}
}

var _money_timer := 0.0

@onready var hp_bar = $HitPoint
@onready var money_label: Label = $MoneyDisplay
@onready var score_label: Label = $ScoreDisplay

@onready var tilemap: TileMapLayer = $SubViewportContainer/SubViewport/TileMapLayer
@onready var tower_manager: Node2D = $TowerManager

@onready var tower_ui := $CanvasLayer2/TowerUI


func _ready():
	preview_tower = tower_scene.instantiate()
	preview_tower.is_preview = true
	$SubViewportContainer/SubViewport.add_child(preview_tower)
	preview_tower.hide()
	hp_bar.max_value = max_hp
	hp_bar.value = max_hp


func _process(_delta):
	# preview tower
	if not is_ai:
		var mouse_pos = get_global_mouse_position()
		var cell = tilemap.local_to_map(tilemap.to_local(mouse_pos))
		var world_pos = tilemap.map_to_local(cell)

		if not tower_ui.visible:
			preview_tower.global_position = tilemap.to_global(world_pos)
			preview_tower.visible = _handle_visibility_of_preview_tower()

		var valid = can_place_tower(cell)
		set_tower_color(preview_tower, valid)

	money_label.text = "Money  :  $ " + str(money)
	_money_timer += _delta
	if _money_timer > 1.0:
		money += money_per_second
		_money_timer = 0.0


# place tower


func set_tower_color(tower: Node2D, is_valid: bool):
	var color = Color(0, 1, 0, 0.5) if is_valid else Color(1, 0, 0, 0.5)
	for child in tower.get_children():
		if child is CanvasItem:
			child.modulate = color


func _unhandled_input(event: InputEvent):
	if not is_ai:
		if (
			event is InputEventMouseButton
			and event.pressed
			and event.button_index == MOUSE_BUTTON_LEFT
		):
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


func _handle_visibility_of_preview_tower():
	# Not visible if money is not enough
	if money < TOWER_COST:
		return false
	return true


func place_tower(cell: Vector2i):
	money -= TOWER_COST
	var tower = tower_scene.instantiate()
	var world_pos = tilemap.map_to_local(cell)
	tower.global_position = tilemap.to_global(world_pos)
	tower.connect("tower_selected", self._on_tower_selected)
	occupied_cells[cell] = true
	tower_manager.add_child(tower)


# update values


func upgrade_income() -> void:
	if money >= cost:
		money_per_second += 1
		money -= cost
		cost += 30


func set_hit_point(damage: int):
	hp_bar.value -= damage


# skills


func start_cooldown(skill: int, cd: float):
	cooldown[skill] = Time.get_unix_time_from_system() + cd


func is_on_cooldown(skill: int) -> bool:
	return cooldown[skill] > Time.get_unix_time_from_system()


func slow_down_enemy():
	var skill_cost: int = 50
	var cd: float = 15.0
	if money < skill_cost or is_on_cooldown(SKILL_SLOW):
		return

	money -= skill_cost
	start_cooldown(SKILL_SLOW, cd)

	# traverse over enemies on selfside
	for path_follow in $OpponentPath.get_children():
		for enemy in path_follow.get_children():
			enemy.slow_down()

	for path_follow in $SystemPath.get_children():
		for enemy in path_follow.get_children():
			enemy.slow_down()


func aoe_damage():
	var skill_cost: int = 100
	var cd: float = 60.0
	if money < skill_cost or is_on_cooldown(SKILL_AOE):
		return

	money -= skill_cost
	start_cooldown(SKILL_AOE, cd)
	var enemies := get_tree().get_nodes_in_group("enemies")
	enemies.sort_custom(
		func(a, b): return a.path_follow.progress_ratio > b.path_follow.progress_ratio
	)
	for i in range(min(enemies.size(), 5)):
		enemies[i].take_damage(50)


func enemy_selected(enemy: String):
	if money < enemy_list[enemy].cost:
		return
	money -= enemy_list[enemy].cost
	money_per_second += enemy_list[enemy].income
	print("Enemy selected:", enemy)


# TowerUI


func _on_tower_selected(tower):
	tower_ui.global_position = tower.global_position
	tower_ui.visible = true
