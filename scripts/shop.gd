extends Control

var enemy_list = [
	{
		name = "plane",
		icon_path =
		"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile270.png"
	},
	{
		name = "tank",
		icon_path = "res://assets/kenney_tower-defense-top-down/PNG/Retina/towerDefense_tile204.png"
	},
	{
		name = "robot",
		icon_path =
		"res://.godot/imported/towerDefense_tile245.png-a634484bb16333c0b20a93f4d77d94ba.ctex"
	}
]

@onready var enemy_grid = $ShopPanel/VBoxContainer/MarginContainer/EnemyList
@onready var panel = $ShopPanel
@onready var open_button = $OpenButton
@onready var close_button = $ShopPanel/VBoxContainer/MarginContainer2/CloseButton


func switch_panel_mode():
	panel.visible = !panel.visible
	panel.mouse_filter = Control.MOUSE_FILTER_STOP if panel.visible else Control.MOUSE_FILTER_IGNORE
	open_button.visible = !open_button.visible


func _ready():
	enemy_grid.custom_minimum_size = Vector2(300, 900)
	for enemy in enemy_list:
		var btn = TextureButton.new()
		var tex = load(enemy.icon_path)
		btn.texture_normal = tex
		#btn.expand_icon = true
		btn.stretch_mode = TextureButton.STRETCH_SCALE
		btn.custom_minimum_size = Vector2(150, 100)
		btn.name = enemy.name

		btn.pressed.connect(_on_avatar_pressed.bind(enemy.name))
		enemy_grid.add_child(btn)

	self.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.visible = false
	open_button.pressed.connect(_on_open_button_pressed)
	close_button.pressed.connect(_on_close_button_pressed)


func _on_avatar_pressed(avatar_name: String):
	print("Avatar selected:", avatar_name)


func _on_close_button_pressed():
	switch_panel_mode()


func _on_open_button_pressed():
	switch_panel_mode()
