extends Control
@onready var enemy_grid = $AttackPanel/MarginContainer/EnemyList
@onready var panel = $AttackPanel
@onready var open_button = $OpenButton
@onready var close_button = $AttackPanel/CloseButton

var enemy_list = [
	{name = "Knight", icon_path = "res://.godot/imported/towerDefense_tile245.png-a634484bb16333c0b20a93f4d77d94ba.ctex"},
	{name = "Mage", icon_path = "res://.godot/imported/towerDefense_tile245.png-a634484bb16333c0b20a93f4d77d94ba.ctex"},
	{name = "Robot", icon_path = "res://.godot/imported/towerDefense_tile245.png-a634484bb16333c0b20a93f4d77d94ba.ctex"}
]

func switch_panel_mode():
	panel.visible = !panel.visible
	open_button.disabled = !open_button.disabled
	close_button.disabled = !close_button.disabled

func _ready():
	for enemy in enemy_list:
		var btn = TextureButton.new()
		var tex = load(enemy.icon_path)
		btn.texture_normal = tex
		btn.custom_minimum_size = Vector2(150, 100)
		btn.name = enemy.name

		btn.pressed.connect(_on_avatar_pressed.bind(enemy.name))
		enemy_grid.add_child(btn)
	
	panel.visible = false
	open_button.disabled = false
	close_button.disabled = true
	open_button.pressed.connect(_on_open_button_pressed)
	close_button.pressed.connect(_on_close_button_pressed)

func _on_avatar_pressed(avatar_name: String):
	print("Avatar selected:", avatar_name)
func _on_close_button_pressed():
	switch_panel_mode()
func _on_open_button_pressed():
	switch_panel_mode()
