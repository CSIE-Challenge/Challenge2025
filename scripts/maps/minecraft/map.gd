extends Map


func _ready():
	#pass
	Engine.time_scale = 4


func _on_area_2d_area_entered(enemy: Area2D) -> void:
	if "max_speed" in enemy:
		enemy.max_speed *= 2


func _on_area_2d_area_exited(_enemy: Area2D) -> void:
	pass


func _on_regen_timer_timeout() -> void:
	var enemies: Array[Area2D] = $Area2D.get_overlapping_areas()
	for e in enemies:
		if "max_speed" in e:
			e.health = min(e.max_health, e.health * 1.2)


func _on_minecart_timer_timeout() -> void:
	$TntMinecart.position = Vector2(-77, 300)
	$TntMinecart.visible = true
	$TntMinecart.end = randf_range(200, 700)
