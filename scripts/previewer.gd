class_name Previewer
extends Node2D

signal selected(position: Vector2)

enum PreviewMode {
	DEFAULT,
	SUCCESS,
	FAIL,
}

var range_circle = null
var _previewed_node: Node

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
	return _map.global_to_local(mouse_pos)


func _init(previewed_node: Node, mode_callback: Callable, map: Map, snap_to_cells: bool) -> void:
	_previewed_node = previewed_node
	_mode_callback = mode_callback
	_map = map
	_snap_to_cells = snap_to_cells
	range_circle = TowerPreviewRange.new(_previewed_node.aim_range / 2)
	_previewed_node.add_child(range_circle)
	self.add_child(previewed_node)


# The previewed object should not intercepts input events before GUI since it will be otherwise not
# intuitive. For example, when a tower preview is active and the player clicks to buy a (possibly
# different) tower, the player should expect the button is pressed and the preview changed
# accordingly. Therefore, this should use _unhandled_input.
func _unhandled_input(event: InputEvent) -> void:
	# left-clicked: select the current mouse position, or cancel if it is out of bounds
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var mouse_pos: Vector2 = _get_selected_position()
		if _map.get_local_terrain(mouse_pos) == Map.CellTerrain.OUT_OF_BOUNDS:
			selected.emit(null)
		else:
			_previewed_node.remove_child(range_circle)
			self.remove_child(_previewed_node)
			selected.emit(mouse_pos)
		get_viewport().set_input_as_handled()
		self.queue_free()


# Now right click should be over everything since it has nothing to do with the GUI
func _input(event: InputEvent) -> void:
	# right-clicked: cancel
	if (
		event is InputEventMouseButton
		and event.pressed
		and event.button_index == MOUSE_BUTTON_RIGHT
	):
		get_viewport().set_input_as_handled()
		_previewed_node.queue_free()
		self.queue_free()


func _process(_delta: float) -> void:
	var mouse_pos = _get_global_mouse_snapped()
	self.global_position = mouse_pos
	var mode: PreviewMode = _mode_callback.call(_previewed_node, _get_selected_position())
	match mode:
		PreviewMode.DEFAULT:
			modulate = Color(1, 1, 1, 0.2)
		PreviewMode.SUCCESS:
			modulate = Color(0, 1, 0, 0.5)
		PreviewMode.FAIL:
			modulate = Color(1, 0, 0, 0.5)
