class_name SpaceMap
extends Map

const OVERLAY_SCORE_THRESHOLD = 25_000

var is_overlay_enabled := false
var overlay_start_us: int


func _ready():
	super()


func get_enemy_z_index(enemy: Enemy) -> int:
	if enemy.path_follow.get_parent() == $OpponentPath:
		return 12  # orange is 11
	if (
		enemy.path_follow.get_parent() == $FlyingOpponentPath
		or enemy.path_follow.get_parent() == $FlyingSystemPath
	):
		return 14  # three paths are 0, 11, 13

	if enemy.path_follow.progress_ratio < 0.35:  # lower path
		return 10
	if enemy.path_follow.progress_ratio < 0.7:  # upper path
		return 14
	if enemy.path_follow.progress_ratio < 0.825:  # lower path
		return 10
	return 14  # upper path


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
