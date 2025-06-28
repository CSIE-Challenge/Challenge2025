extends CanvasLayer

@onready var upgrade_button: Button = $Upgrade
@onready var slow_button: Button = $SkillSlow
@onready var aoe_button: Button = $AoeDamage
@onready var shop: Control = $Shop
@onready var game: Node2D = $"../LeftPlayer"


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass  # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	upgrade_button.text = "cost $%d to upgrade" % game.cost
	slow_button.text = (
		"slow down enemies (CD: %.2f)"
		% maxf(0.0, game.cooldown[game.SKILL_SLOW] - Time.get_unix_time_from_system())
	)
	aoe_button.text = (
		"damage on fastest 5 enemies (CD: %.2f)"
		% maxf(0.0, game.cooldown[game.SKILL_AOE] - Time.get_unix_time_from_system())
	)


func _on_upgrade_pressed() -> void:
	game.upgrade_income()


func _on_skill_slow_pressed() -> void:
	game.slow_down_enemy()


func _on_aoe_damage_pressed() -> void:
	game.aoe_damage()
