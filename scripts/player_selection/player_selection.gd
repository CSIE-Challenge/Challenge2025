extends Control

const ROUND_SCENE = preload("res://scenes/round.tscn")

@onready var selection_1p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection1P
@onready var selection_2p: IndividualPlayerSelection = $VBoxContainer/HBoxContainer/Selection2P


func _ready() -> void:
	selection_1p.manual_control_enabled.connect(func(): selection_2p.manual_control = false)
	selection_2p.manual_control_enabled.connect(func(): selection_1p.manual_control = false)


func _on_start_button_pressed() -> void:
	var manual_controlled = 0
	if selection_1p.manual_control:
		manual_controlled = 1
	if selection_2p.manual_control:
		manual_controlled = 2
