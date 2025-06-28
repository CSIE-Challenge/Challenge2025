extends Control

@onready var enemy_grid = $ShopPanel/VBoxContainer/MarginContainer/EnemyList
@onready var panel = $ShopPanel
@onready var open_button = $OpenButton
@onready var close_button = $ShopPanel/VBoxContainer/MarginContainer2/CloseButton
@onready var game = $"../../LeftPlayer"  # Game scene
@onready var enemy_list = game.enemy_list


func switch_panel_mode():
	panel.visible = !panel.visible
	panel.mouse_filter = Control.MOUSE_FILTER_STOP if panel.visible else Control.MOUSE_FILTER_IGNORE
	open_button.visible = !open_button.visible


func _ready():
	enemy_grid.custom_minimum_size = Vector2(300, 900)
	for enemy in enemy_list:
		_spawn_button(enemy)

	self.mouse_filter = Control.MOUSE_FILTER_IGNORE
	panel.visible = false
	open_button.pressed.connect(_on_open_button_pressed)
	close_button.pressed.connect(_on_close_button_pressed)


func _on_enemy_pressed(enemy: String):
	game.enemy_selected(enemy)


func _on_close_button_pressed():
	switch_panel_mode()


func _on_open_button_pressed():
	switch_panel_mode()


func _spawn_button(enemy: String):
	var btn = Button.new()
	btn.custom_minimum_size = Vector2(150, 225)
	btn.flat = true
	btn.name = enemy

	# For formatting
	var vbox = VBoxContainer.new()
	vbox.alignment = BoxContainer.ALIGNMENT_CENTER
	vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL

	# Picture
	var tex = TextureRect.new()
	tex.texture = load(enemy_list[enemy].icon_path)
	tex.stretch_mode = TextureRect.STRETCH_SCALE
	tex.custom_minimum_size = Vector2(150, 150)
	vbox.add_child(tex)

	# Word Label
	var cost_label = Label.new()
	cost_label.text = "Cost: %d" % enemy_list[enemy].cost
	cost_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	cost_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	vbox.add_child(cost_label)

	var income_label = Label.new()
	income_label.text = "Income: %d" % enemy_list[enemy].income
	income_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	income_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	vbox.add_child(income_label)

	btn.add_child(vbox)

	btn.pressed.connect(_on_enemy_pressed.bind(enemy))
	enemy_grid.add_child(btn)
