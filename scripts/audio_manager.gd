extends Node

@onready var enemy_attack: AudioStreamPlayer = $EnemyAttack
@onready var enemy_die: AudioStreamPlayer = $EnemyDie
@onready var enemy_move: AudioStreamPlayer = $EnemyMove  # loop
@onready var background_game: AudioStreamPlayer = $BackgroundGame  # loop
@onready var background_menu: AudioStreamPlayer = $BackgroundMenu  # loop
@onready var button_on_click: AudioStreamPlayer = $ButtonOnClick
@onready var tower_place: AudioStreamPlayer = $TowerPlace
@onready var tower_shoot: AudioStreamPlayer = $TowerShoot
@onready var upgrade: AudioStreamPlayer = $Upgrade
