class_name Enemy
extends Area2D

enum EnemyType {
	BUZZY_BEETLE,
	GOOMBA,
	KOOPA_JR,
	KOOPA_PARATROOPA,
	KOOPA,
	SPINY_SHELL,
	WIGGLER,
}

@export var type: EnemyType
@export var income_impact: int = 0
@export var max_health: int = 100
# Note that the speed of enemy should never exceed that of explosion of effect,
# error may occur otherwise
@export var max_speed: int = 50
@export var damage: int = 5
@export var flying: bool = false
@export var knockback_resist: bool = false
@export var kill_reward: int = 1
@export var summon_cooldown: float = 2.0

var game: Game
var path_follow: PathFollow2D
var knockback_distance: int = 25
var source: Game.EnemySource
var health: int:
	get:
		return health
	set(value):
		health = value
		if health_bar != null:
			health_bar.value = health / float(max_health) * 100.0
var freeze_debuff: Array[float] = [1.0]  # store all effects, minimum of the array is applied
var knockback_invincibility = false

@onready var sprite = $AnimatedSprite2D
@onready var health_bar := $HealthBar


func _on_killed() -> void:
	game.kill_count += 1
	path_follow.queue_free()


func _on_reached() -> void:
	game.take_damage(damage)
	AudioManager.enemy_attack.play()
	path_follow.queue_free()


func take_damage(amount: int):
	health -= amount
	if health <= 0:
		if source == Game.EnemySource.SYSTEM:
			game.score += kill_reward  # == 0.1 * damage
			game.money += kill_reward
			game.money_earned += kill_reward
			if not game.during_boo:
				game.display_kill_reward += kill_reward
			game.kill_reward_within_second += kill_reward
		_on_killed()


# TODO: to delete, already implemented in bullet.gd
func _on_area_entered(bullet: Bullet) -> void:
	if not bullet.alive:
		return
	take_damage(bullet.damage)
	bullet._on_hit()

	match bullet.effect:
		bullet.Effect.FREEZE:
			freeze(0.7)
		bullet.Effect.DEEP_FREEZE:
			freeze(0.5)
		bullet.Effect.KNOCKBACK:
			knockback(false)
		bullet.Effect.FAR_KNOCKBACK:
			knockback(true)


#region Effect


func knockback(far: bool):
	if knockback_invincibility or ((not knockback_resist) and (not far)):
		return
	knockback_invincibility = true
	if far:
		if knockback_resist:
			path_follow.progress -= knockback_distance
		else:
			path_follow.progress -= knockback_distance * 2
	else:
		if not knockback_resist:
			path_follow.progress -= knockback_distance
	await get_tree().create_timer(3).timeout
	knockback_invincibility = false


func freeze(rate: float):
	# simply append it
	freeze_debuff.append(rate)
	await get_tree().create_timer(1).timeout
	freeze_debuff.erase(rate)


#region Spells


func transport():
	var op_game = game.op_game
	path_follow.get_parent().remove_child(path_follow)
	if flying:
		op_game.map.flying_opponent_path.add_child(path_follow)
	else:
		op_game.map.opponent_path.add_child(path_follow)
	path_follow.progress_ratio = 0

	# Swap games so scores are calculated correcrtly
	var tmp_game = op_game
	op_game = game
	game = tmp_game


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


func _process(delta):
	path_follow.progress += freeze_debuff.min() * max_speed * delta
	if path_follow.progress_ratio >= 0.99:
		_on_reached()

	self.z_index = game.map.get_enemy_z_index(self)

	self.rotation = -path_follow.rotation
	if cos(path_follow.rotation) > 0:
		sprite.flip_h = true
	if cos(path_follow.rotation) < 0:
		sprite.flip_h = false
