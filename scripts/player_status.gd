extends TextureRect

var player_selection: IndividualPlayerSelection

# 0: showing money. 1: showing api quota
var active_item: int = 0


func _init() -> void:
	# keep updating connection status (the signal light) when the game is paused
	process_mode = Node.PROCESS_MODE_ALWAYS


func _toggle_money_quota(show_quota: bool) -> void:
	$Coin.visible = not show_quota
	$Money.visible = not show_quota
	$Income.visible = not show_quota
	$KillReward.visible = not show_quota
	$ApiQuotaIcon.visible = show_quota
	$ApiQuota.visible = show_quota
	active_item = show_quota as int


# repsonsible for alternately showing money and API quota
func _on_switching_timer_timeout() -> void:
	match active_item:
		0:
			_toggle_money_quota(true)
			$SwitchingTimer.start(1.5)
		1:
			_toggle_money_quota(false)
			$SwitchingTimer.start(4)


func link_player_selection(_player_selection: IndividualPlayerSelection) -> void:
	# add and hide the player selection panel
	player_selection = _player_selection
	$CanvasLayer.add_child(player_selection)
	player_selection.visible = false

	# toggle player selection panel when the indicator is clicked
	var toggle_selection_panel = func(): player_selection.visible = not player_selection.visible
	$StatusConnected.pressed.connect(toggle_selection_panel)
	$StatusDisconnected.pressed.connect(toggle_selection_panel)


func _process(_delta: float) -> void:
	player_selection.global_position = Vector2(global_position.x, global_position.y + size.y)

	# display connection status with red/green lights
	var agent_connected = player_selection.web_agent._ws.is_client_connected()
	$StatusConnected.visible = agent_connected
	$StatusDisconnected.visible = not agent_connected
