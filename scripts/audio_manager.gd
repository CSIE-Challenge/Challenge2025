extends Node

@onready var enemy_attack: AudioStreamPlayer = $EnemyAttack
@onready var enemy_die: AudioStreamPlayer = $EnemyDie
@onready var enemy_move: AudioStreamPlayer = $EnemyMove  # loop
@onready var background_game_stage1: AudioStreamPlayer = $BackgroundGameStage1  # loop
@onready var background_game_stage2: AudioStreamPlayer = $BackgroundGameStage2  # loop
@onready var background_menu: AudioStreamPlayer = $BackgroundMenu  # loop
@onready var button_on_click: AudioStreamPlayer = $ButtonOnClick
@onready var tower_place: AudioStreamPlayer = $TowerPlace
@onready var tower_shoot: AudioStreamPlayer = $TowerShoot
