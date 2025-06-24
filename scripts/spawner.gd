extends Node2D

@export var enemy_scene: PackedScene
@export var spawn_interval := 2.0 # Should be gcd of all possible spawning interval?
@export var max_opponent_enemy := 20
@export var max_system_enemy := 20

var opponent_enemy_spawned := 0
var system_enemy_spawned := 0

@onready var spawn_timer: Timer = $Timer
enum EnemySource {
	SYSTEM,
	OPPONENT
}
@onready var system_path: Path2D = $"../SystemPath"
@onready var opponent_path: Path2D = $"../OpponentPath"

func _ready():
	spawn_timer.wait_time = spawn_interval
	spawn_timer.timeout.connect(_on_spawn_timeout)
	spawn_timer.start()

# Seperate the spawn function for system and opponent in case special needed later
func spawn_enemy(ratio: float, path:Path2D, type: EnemySource):
	var enemy = enemy_scene.instantiate()
	var path_follow = PathFollow2D.new()
	path.add_child(path_follow)
	path_follow.progress_ratio = ratio
	path_follow.loop = false
	path_follow.add_child(enemy)
	match type:
		EnemySource.SYSTEM:
			system_enemy_spawned += 1
		EnemySource.OPPONENT:
			opponent_enemy_spawned += 1

func spawn_system_enemy():
	spawn_enemy(0.0, system_path, EnemySource.SYSTEM)

func spawn_opponent_enemy():
	spawn_enemy(0.0, opponent_path, EnemySource.OPPONENT)

func _on_spawn_timeout():
	if system_enemy_spawned >= max_system_enemy and \
		opponent_enemy_spawned >= max_opponent_enemy:
		
		spawn_timer.stop()
		return
	if system_enemy_spawned < max_system_enemy:
		spawn_system_enemy()
	if opponent_enemy_spawned < max_opponent_enemy:
		spawn_opponent_enemy()
