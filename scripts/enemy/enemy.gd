class_name Enemy
extends Area2D

@export var max_health: int = 100
# Note that the speed of enemy should never exceed that of explosion of effect,
# error may occur otherwise
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
var knockback_ratio: float = 0.1
var source: Game.EnemySource
var health: int:
	get:
		return health
	set(value):
		health = value
		if health_bar != null:
			health_bar.value = health / float(max_health) * 100.0
var speed_rate: Array[float] = [1.0]  # store speed_rates and get minimum

@onready var sprite = $AnimatedSprite2D
@onready var health_bar := $HealthBar


func _on_killed() -> void:
	game.income_per_second += kill_reward  # or game.money
	path_follow.queue_free()


func _on_reached() -> void:
	game.damage_taken.emit(damage)
	path_follow.queue_free()


func take_damage(amount: int):
	if shield == 0:
		health -= amount * max(0.2, (20.0 - armor) / 20.0)
	else:
		shield -= min(amount, shield)

	if health <= 0:
		_on_killed()


# TODO: to delete, already implemented in bullet.gd
func _on_area_entered(bullet: Bullet) -> void:
	if not bullet.alive:
		return
	take_damage(bullet.damage)
	bullet._on_hit()

	match bullet.effect:
		bullet.Effect.FREEZE:
			freeze(0.6)
		bullet.Effect.DEEP_FREEZE:
			freeze(0.3)
		bullet.Effect.KNOCKBACK:
			knockback(false)
		bullet.Effect.FAR_KNOCKBACK:
			knockback(true)


#region Effect


func knockback(far: bool):
	if far:
		if knockback_resist:
			path_follow.progress_ratio -= knockback_ratio
		else:
			path_follow.progress_ratio -= knockback_ratio * 2
	else:
		if not knockback_resist:
			path_follow.progress_ratio -= knockback_ratio


func freeze(rate: float):
	speed_rate.append(rate)
	await get_tree().create_timer(8).timeout
	speed_rate.erase(rate)


#region Spells


func transport():
	var op_game = game.op_game
	path_follow.get_parent().remove_child(path_follow)
	# TODO: for flying enemy, add_child to flying path
	op_game._map.opponent_path.add_child(path_follow)
	path_follow.progress_ratio = 0


#endregion


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
	$AnimatedSprite2D.play("default")
	self.z_index = 10  # For effect to be on the ground


func _process(delta):
	path_follow.progress += speed_rate.min() * max_speed * delta
	if path_follow.progress_ratio >= 0.99:
		_on_reached()

	self.rotation = -path_follow.rotation
	if cos(path_follow.rotation) > 0:
		sprite.flip_h = true
	if cos(path_follow.rotation) < 0:
		sprite.flip_h = false
