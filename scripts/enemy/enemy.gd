class_name Enemy
extends Area2D

@export var max_health: int = 100
@export var max_speed: int = 50
@export var flying: bool = false
@export var damage: int = 5
@export var armor: int = 0
@export var shield: int = 0
@export var knockback_resist: bool = false
@export var kill_reward: int = 0
@export var income_impact: int = 0

var game: Game
var path_follow: PathFollow2D
var source: Game.EnemySource
var health: int:
	get:
		return health
	set(value):
		health = value
		if health_bar != null:
			health_bar.value = health / float(max_health) * 100.0

@onready var health_bar := $HealthBar


func _on_killed() -> void:
	path_follow.queue_free()


func _on_reached() -> void:
	game.damage_taken.emit(damage)
	path_follow.queue_free()


func take_damage(amount: int):
	health -= amount
	if health <= 0:
		_on_killed()


func _on_area_entered(bullet: Bullet) -> void:
	if not bullet.alive:
		return
	bullet.alive = false
	take_damage(bullet.damage)
	bullet.queue_free()


# _init not overridden because PackedScene.instantiate() does not accept arguments
func init(_source: Game.EnemySource) -> void:
	source = _source
	path_follow = PathFollow2D.new()
	path_follow.loop = false
	path_follow.add_child(self)
	$HealthBar.visible = true


func _ready():
	health = max_health
	if path_follow != null:
		path_follow.progress_ratio = 0
	add_to_group("enemies")


func _process(delta):
	path_follow.progress += max_speed * delta
	if path_follow.progress_ratio >= 0.99:
		_on_reached()
	if health_bar != null:
		health_bar.rotation = -path_follow.rotation
