extends Node2D

@export var enemy_scene: PackedScene
@export var spawn_interval := 2.0
@export var max_enemies := 20

var enemies_spawned := 0

@onready var spawn_timer: Timer = $Timer
@onready var path: Path2D = $"../ComputerPath"


func _ready():
	spawn_timer.wait_time = spawn_interval
	spawn_timer.timeout.connect(_on_spawn_timeout)
	spawn_timer.start()


func _on_spawn_timeout():
	if enemies_spawned >= max_enemies:
		spawn_timer.stop()
		return

	var enemy = enemy_scene.instantiate()
	var path_follow = PathFollow2D.new()
	path.add_child(path_follow)

	path_follow.progress_ratio = 0.0
	path_follow.loop = false
	path_follow.add_child(enemy)

	enemies_spawned += 1
