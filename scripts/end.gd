class_name EndScreen
extends Control

const ALIGN_LEFT = HORIZONTAL_ALIGNMENT_LEFT
const ALIGN_CENTER = HORIZONTAL_ALIGNMENT_CENTER
const ALIGN_RIGHT = HORIZONTAL_ALIGNMENT_RIGHT

const DISPLAY_STATS = 6
# [400 160 720 160 400] x 120
const ROW_MARGIN = 20
const ROW_HEIGHT = 100
const WINNER_ROW_HEIGHT = 120
const ROW_STATS_WIDTH = 400
const ROW_DIFF_STATS_WIDTH = 160
const ROW_TITLE_WIDTH = 720

var player_names: Array[String] = []
var statistics: Array[Statistics] = []

@onready var remaining_height = (
	$MarginContainer/VBoxContainer.size.y - $MarginContainer/VBoxContainer/PlayerRow.size.y
)


class RichTextLabelBuilder:
	var height: int = ROW_HEIGHT
	var width: int
	var text: String
	var font_size: int
	var font_color := Color(1, 1, 1)
	var align: HorizontalAlignment
	var bg_color := Color(0, 0, 0, 0)
	var border: int

	static func plain(stat: String, _width: int, side: HorizontalAlignment) -> RichTextLabelBuilder:
		var builder := RichTextLabelBuilder.new()
		builder.width = _width
		builder.text = stat
		builder.font_size = 64
		builder.align = side
		builder.border = 20
		return builder

	static func title(stat: String, important: bool) -> RichTextLabelBuilder:
		var builder := RichTextLabelBuilder.plain(stat, ROW_TITLE_WIDTH, ALIGN_CENTER)
		var alpha = 1.0 if important else 0.4
		builder.bg_color = Color(0.5, 0.5, 0.5, alpha)
		return builder

	static func raw_stat(stat: String, side: HorizontalAlignment):
		return RichTextLabelBuilder.plain(stat, ROW_STATS_WIDTH, side)

	static func diff_stat(stat: String, side: HorizontalAlignment, invert: bool):
		var builder := RichTextLabelBuilder.new()
		builder.width = ROW_DIFF_STATS_WIDTH
		builder.text = stat
		builder.font_size = 32
		builder.border = 0
		if (stat.begins_with("+") and !invert) or (stat.begins_with("-") and invert):
			builder.font_color = Color(0.2, 1, 0.2)
		if (stat.begins_with("-") and !invert) or (stat.begins_with("+") and invert):
			builder.font_color = Color(1, 0.2, 0.2)
		builder.align = side
		return builder

	func build() -> RichTextLabel:
		var stylebox = StyleBoxFlat.new()
		stylebox.bg_color = self.bg_color
		stylebox.border_width_left = self.border
		stylebox.border_width_right = self.border
		stylebox.border_color = Color(0, 0, 0, 0)
		var label = RichTextLabel.new()
		label.custom_minimum_size = Vector2(self.width, self.height)
		label.horizontal_alignment = self.align
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.size_flags_horizontal = Control.SizeFlags.SIZE_FILL | Control.SizeFlags.SIZE_EXPAND
		label.add_theme_stylebox_override("normal", stylebox)
		label.push_color(self.font_color)
		label.push_font_size(self.font_size)
		label.add_text(self.text)
		label.pop_all()
		return label


class Statistics:
	var title: String
	var player_scores: Array[int]
	# If a statistics is important, it will always be displayed and determines the outcome
	# These statistics is determined in the passed order.
	var important: bool
	# Inverts the result. For example, API call should be the less the better
	var invert: bool
	# If true, the difference will be displayed with ratio instead
	var compare_with_ratio: bool

	static func init(
		_title: String,
		scores: Array[int],
		is_important: bool,
		should_invert: bool = false,
		display_ratio: bool = false
	) -> Statistics:
		var stat = Statistics.new()
		stat.title = _title
		stat.player_scores = scores
		stat.important = is_important
		stat.invert = should_invert
		stat.compare_with_ratio = display_ratio
		return stat


func _append_row(
	builders: Array[RichTextLabelBuilder],
	top_margin: int = ROW_MARGIN,
	bottom_margin: int = ROW_MARGIN
) -> void:
	var vbox_container := $MarginContainer/VBoxContainer
	var margin_container := MarginContainer.new()
	var hbox_container := HBoxContainer.new()
	margin_container.custom_minimum_size.y = ROW_HEIGHT
	margin_container.add_theme_constant_override("margin_top", top_margin)
	margin_container.add_theme_constant_override("margin_bottom", bottom_margin)
	hbox_container.add_theme_constant_override("seperation", 0)
	for builder in builders:
		hbox_container.add_child(builder.build())
	margin_container.add_child(hbox_container)
	vbox_container.add_child(margin_container)
	remaining_height -= margin_container.size.y


func _build_winner_row(side: HorizontalAlignment):
	var vbox_container: VBoxContainer = $MarginContainer/VBoxContainer
	var builder = RichTextLabelBuilder.plain(
		"Winner!" if side != ALIGN_CENTER else "Tied", vbox_container.size.x as int, side
	)
	builder.font_color = Color(1, 1, 0)
	builder.font_size = 96
	builder.height = WINNER_ROW_HEIGHT
	_append_row([builder], remaining_height - WINNER_ROW_HEIGHT, 0)


func compute_diff(score: int, opponent: int, use_ratio: bool) -> String:
	if score == opponent:
		return "="
	# Regular: absolute difference
	if not use_ratio:
		var diff = score - opponent
		if diff < 0:
			return "%d" % diff
		return "+%d" % diff

	# Ratio
	if opponent == 0:
		return "+∞%"
	var ratio_diff = (float(score) / opponent - 1.0) * 100
	if ratio_diff < 0:
		return "%.0f%%" % ratio_diff
	return "+%.0f%%" % ratio_diff


func _append_row_from_stat(stat: Statistics):
	var left_diff_str = compute_diff(
		stat.player_scores[0], stat.player_scores[1], stat.compare_with_ratio
	)
	var right_diff_str = compute_diff(
		stat.player_scores[1], stat.player_scores[0], stat.compare_with_ratio
	)

	var builders: Array[RichTextLabelBuilder] = [
		RichTextLabelBuilder.raw_stat("%d" % stat.player_scores[0], ALIGN_LEFT),
		RichTextLabelBuilder.diff_stat(left_diff_str, ALIGN_RIGHT, stat.invert),
		RichTextLabelBuilder.title(stat.title, stat.important),
		RichTextLabelBuilder.diff_stat(right_diff_str, ALIGN_LEFT, stat.invert),
		RichTextLabelBuilder.raw_stat("%d" % stat.player_scores[1], ALIGN_RIGHT),
	]
	_append_row(builders)


func _build():
	var winning_side: HorizontalAlignment = ALIGN_CENTER
	var remaining_stats: Array[Statistics]
	var slots = DISPLAY_STATS
	for stat in statistics:
		if stat.important:
			if stat.player_scores[0] != stat.player_scores[1] and winning_side == ALIGN_CENTER:
				# I hate Godot, why is there no XOR ???
				if (stat.player_scores[0] > stat.player_scores[1]) != stat.invert:
					winning_side = ALIGN_LEFT
				else:
					winning_side = ALIGN_RIGHT

			assert(slots > 0)
			_append_row_from_stat(stat)
			slots -= 1
		else:
			# [0, 0] will break sorting and is not interesting so just yeet 'em out
			if stat.player_scores != [0, 0]:
				remaining_stats.append(stat)

	remaining_stats.sort_custom(
		func(a: Statistics, b: Statistics):
			return (
				float(a.player_scores.max()) / a.player_scores.min()
				> float(b.player_scores.max()) / b.player_scores.min()
			)
	)

	for stat in remaining_stats:
		if slots > 0:
			_append_row_from_stat(stat)
			slots -= 1
	_build_winner_row(winning_side)


func _ready() -> void:
	# fill in player names
	$MarginContainer/VBoxContainer/PlayerRow/LeftPlayerName.text = player_names[0]
	$MarginContainer/VBoxContainer/PlayerRow/RightPlayerName.text = player_names[1]

	# setup stat entries
	_build()


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		get_tree().quit()
