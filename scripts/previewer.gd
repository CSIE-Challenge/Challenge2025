class_name Previewer
extends Node2D


signal selected(position: Vector2)


enum PreviewMode {
	DEFAULT,
	SUCCESS,
	FAIL,
}


# this is called every frame for updating the color of previewed object
# function signature should be `(Vector2) -> PreviewMode` when _snap_to_cells is false,
# or `(Vector2i) -> PreviewMode` when _snap_to_cells is true
var _mode_callback: Callable

# the returned coordinates (or cell positions) are in the local coordinate of this map
var _map: Map

# if not null, the mouse position will be snapped to the centers of the cells
var _snap_to_cells: bool


func _get_global_mouse_snapped() -> Vector2:
	var mouse_pos = get_global_mouse_position()
	if _snap_to_cells:
		mouse_pos = _map.cell_to_global(_map.global_to_cell(mouse_pos))
	return mouse_pos


func _get_selected_position() -> Vector2:
	var mouse_pos = _get_global_mouse_snapped()
	if _snap_to_cells:
		return _map.global_to_cell(mouse_pos)
	else:
		return _map.global_to_local(mouse_pos)


func _init(previewed_node: Node, mode_callback: Callable, map: Map, snap_to_cells: bool) -> void:
	self.add_child(previewed_node)
	_mode_callback = mode_callback
	_map = map
	_snap_to_cells = snap_to_cells


# the previewed object intercepts input events before GUI, so that (for example)
# when the player clicks on the GUI when previewing, he cancels the previewer
# before the next interaction with the GUI
func _input(event: InputEvent) -> void:
	# left-clicked: select the current mouse position, or cancel if it is out of bounds
	if (
			event is InputEventMouseButton
			and event.pressed
			and event.button_index == MOUSE_BUTTON_LEFT
	):
		var mouse_pos: Vector2 = _get_selected_position()
		if _map.get_local_terrain(mouse_pos) == Map.CellTerrain.OUT_OF_BOUNDS:
			selected.emit(null)
		else:
			selected.emit(mouse_pos)
		get_viewport().set_input_as_handled()
		self.queue_free()
	# ESC pressed: preview cancelled
	if (
			event is InputEventKey
			and event.pressed
			and event.keycode == KEY_ESCAPE
	):
		selected.emit(null)
		get_viewport().set_input_as_handled()
		self.queue_free()


func _process(_delta: float) -> void:
	var mouse_pos = _get_global_mouse_snapped()
	self.global_position = mouse_pos
	var mode: PreviewMode = _mode_callback.call(_get_selected_position())
	match mode:
		PreviewMode.DEFAULT:
			modulate = Color(1, 1, 1, 0.5)
		PreviewMode.SUCCESS:
			modulate = Color(0, 1, 0, 0.5)
		PreviewMode.FAIL:
			modulate = Color(1, 0, 0, 0.5)

