extends TextureRect

var player_selection: IndividualPlayerSelection


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
