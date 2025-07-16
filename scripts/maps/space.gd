class_name SpaceMap
extends Map

const OVERLAY_SCORE_THRESHOLD = 200_000

var is_overlay_enabled := false
var overlay_start_us: int


func _ready():
	super()
	$SystemPathUpperTexture.z_index = Util.H_PATH
	$OpponentPathTexture.z_index = Util.M_PATH
	$SystemPathLowerTexture.z_index = Util.L_PATH


func get_enemy_z_index(enemy: Enemy) -> int:
	if enemy.path_follow.get_parent() == $OpponentPath:
		enemy.health_bar.z_index = 0
		return Util.M_ENEMY
	if (
		enemy.path_follow.get_parent() == $FlyingOpponentPath
		or enemy.path_follow.get_parent() == $FlyingSystemPath
	):
		enemy.health_bar.z_index = Util.TOWER_LAYER  # Set back to default
		return Util.FLYING_LAYER

	if enemy.path_follow.progress_ratio < 0.35:  # lower path
		enemy.health_bar.z_index = 0
		return Util.L_ENEMY
	if enemy.path_follow.progress_ratio < 0.7:  # upper path
		enemy.health_bar.z_index = Util.TOWER_LAYER  # Set back to default
		return Util.ENEMY_LAYER
	if enemy.path_follow.progress_ratio < 0.825:  # lower path
		enemy.health_bar.z_index = 0
		return Util.L_ENEMY
	# upper path
	enemy.health_bar.z_index = 0
	return Util.ENEMY_LAYER


func _process(_delta):
	if !is_overlay_enabled:
		if game.score > OVERLAY_SCORE_THRESHOLD:
			is_overlay_enabled = true
			self.overlay_start_us = Time.get_ticks_usec()
	if is_overlay_enabled:
		var t = (Time.get_ticks_usec() - overlay_start_us) / 1_000_000.0
		var ratio = sin(t * 2 * PI)
		$SystemPathLowerOverlay.modulate = Color(1, 1, 1, abs(ratio))
		$SystemPathUpperOverlay.modulate = Color(1, 1, 1, abs(ratio))
		$OpponentPathOverlay.modulate = Color(1, 1, 1, abs(ratio))
