extends TextureRect


func link_player_selection(player_selection: IndividualPlayerSelection) -> void:
	# add and hide the player selection panel
	$CanvasLayer.add_child(player_selection)
	player_selection.position.y = 80
	player_selection.visible = false

	# display connection status with red/green lights
	player_selection.web_agent._ws.client_connected.connect(
		func():
			$StatusConnected.visible = true
			$StatusDisconnected.visible = false
	)
	player_selection.web_agent._ws.client_disconnected.connect(
		func():
			$StatusConnected.visible = false
			$StatusDisconnected.visible = true
	)

	# toggle player selection panel when the indicator is clicked
	var toggle_selection_panel = func(): player_selection.visible = not player_selection.visible
	$StatusConnected.pressed.connect(toggle_selection_panel)
	$StatusDisconnected.pressed.connect(toggle_selection_panel)
