extends Node

var second_stage := false
var background1_music_position: float
var background2_music_position: float

@onready var enemy_attack: AudioStreamPlayer = $EnemyAttack
@onready var enemy_die: AudioStreamPlayer = $EnemyDie
@onready var enemy_move: AudioStreamPlayer = $EnemyMove  # loop
@onready var background_game_stage1: AudioStreamPlayer = $BackgroundGameStage1  # loop
@onready var background_game_stage2: AudioStreamPlayer = $BackgroundGameStage2  # loop
@onready var background_menu: AudioStreamPlayer = $BackgroundMenu  # loop
@onready var button_on_click: AudioStreamPlayer = $ButtonOnClick
@onready var tower_place: AudioStreamPlayer = $TowerPlace
@onready var tower_shoot: AudioStreamPlayer = $TowerShoot
@onready var bullet_explode: AudioStreamPlayer = $BulletExplode
@onready var match_sound: AudioStreamPlayer = $Match
@onready var macos: AudioStreamPlayer = $MacOS
@onready var windows: AudioStreamPlayer = $Windows
@onready var join: AudioStreamPlayer = $Join
@onready var leave: AudioStreamPlayer = $Leave
@onready var message: AudioStreamPlayer = $Message

@onready var metal_pipe_source: AudioStream = preload("res://assets/audio/metal_pipe.mp3")


func play_metal_pipe() -> void:
	if metal_pipe_source:
		var audio_player: AudioStreamPlayer = AudioStreamPlayer.new()
		audio_player.stream = metal_pipe_source
		add_child(audio_player)
		audio_player.play()
		audio_player.connect("finished", audio_player.queue_free)
	else:
		push_error("Metal pipe sound source is not set.")
