extends Node2D

const TOWER_COST = 5
const SKILL_SLOW = 0
const SKILL_AOE = 1

@export var tower_scene: PackedScene
@export var is_ai: bool
@export var agent_scene: PackedScene

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
	var ws = APIServer.get_instance().register_connection()
	var agent = agent_scene.instantiate()
	agent.link(ws)
	self.add_child(agent)

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
	if money < tower.building_cost:
		return false
	return _map.get_cell_terrain(cell_pos) == Map.CellTerrain.EMPTY


func _on_tower_sold(tower: Tower, tower_ui: TowerUi):
	var refund := tower.upgrade_cost
	money += refund
	tower.queue_free()
	tower_ui.queue_free()
	var cell_pos = _map.global_to_cell(tower.global_position)
	built_towers.erase(cell_pos)


func place_tower(cell_pos: Vector2i, tower: Tower) -> void:
	if not (_is_buildable(tower, cell_pos) and spend(tower.building_cost)):
		return
	var global_pos = _map.cell_to_global(cell_pos)

	self.add_child(tower)
	tower.enable(global_pos)
	built_towers[cell_pos] = tower


func _on_buy_tower(tower_scene: PackedScene):
	var tower = tower_scene.instantiate() as Tower
	var preview_color_callback = func(tower: Tower, cell_pos: Vector2i) -> Previewer.PreviewMode:
		if money >= tower.building_cost and _is_buildable(tower, cell_pos):
			return Previewer.PreviewMode.SUCCESS
		return Previewer.PreviewMode.FAIL

	var previewer = Previewer.new(tower, preview_color_callback, _map, true)
	previewer.selected.connect(self.place_tower.bind(tower))
	self.add_child(previewer)


func _select_tower(tower: Tower):
	var tower_ui: TowerUi = TOWER_UI_SCENE.instantiate()
	self.add_child(tower_ui)
	tower_ui.global_position = tower.global_position
	tower_ui.sold.connect(self._on_tower_sold.bind(tower, tower_ui))


func _handle_tower_selection(event: InputEvent) -> void:
	if not (
		event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed
	):
		return
	var clicked_cell = _map.global_to_cell(get_global_mouse_position())
	if built_towers.has(clicked_cell):
		_select_tower(built_towers[clicked_cell])
		get_viewport().set_input_as_handled()


#endregion

#region Income


func _on_constant_income_timer_timeout() -> void:
	money += income_per_second


#endregion

#region Enemies


func _initialize_enemy_from_data(unit_data: Dictionary) -> Enemy:
	var scene_path = unit_data.get("scene_path")
	if scene_path == null or !ResourceLoader.exists(scene_path):
		print("Attempted to initialize Invalid Enemy Scene (%s)" % scene_path)
		return
	if !_enemy_scene_cache.has(scene_path):
		_enemy_scene_cache[scene_path] = load(scene_path)

	var enemy: Enemy = _enemy_scene_cache[scene_path].instantiate()
	var stats: Dictionary = unit_data.get("stats", {})
	enemy.max_health = stats.max_health
	enemy.max_speed = stats.max_speed
	enemy.damage = stats.damage
	enemy.flying = stats.flying
	return enemy


func _on_enemy_spawn(unit_data: Dictionary) -> void:
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.SYSTEM)


func _on_enemy_summon(unit_data: Dictionary) -> void:
	_deploy_enemy(_initialize_enemy_from_data(unit_data), EnemySource.OPPONENT)


func _deploy_enemy(enemy: Enemy, source: EnemySource) -> void:
	enemy.game = self
	enemy.init(source)
	var path: Path2D
	match source:
		EnemySource.SYSTEM:
			path = _map.system_path
		EnemySource.OPPONENT:
			path = _map.opponent_path
	path.add_child(enemy.path_follow)


#endregion

#region Spells


func _on_spell_deploy(spell_data) -> void:
	print("Spell ", spell_data, " unhandled")


#endregion


func _process(_delta) -> void:
	status_panel.get_child(0).text = "$%d" % money


func _unhandled_input(event: InputEvent) -> void:
	if (
		event is InputEventMouseButton
		and event.button_index == MOUSE_BUTTON_RIGHT
		and event.pressed
		and previewer != null
	):
		previewer.free()
	_handle_tower_selection(event)
