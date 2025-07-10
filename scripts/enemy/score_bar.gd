class_name ScoreBar
extends Container

const MAX_SCORE_DIFF = 1_000_000

var left_score: int
var right_score: int


func _notification(what):
	if what == NOTIFICATION_SORT_CHILDREN:
		_process(0)


func _process(_delta):
	var rect_size = Vector2(size.x / 2, size.y / 8)
	fit_child_in_rect($TopBorder1P, Rect2(Vector2(0, size.y * 7 / 8), rect_size))
	fit_child_in_rect($TopBorder2P, Rect2(Vector2(size.x / 2, size.y * 7 / 8), rect_size))

	var score_diff = min(abs(left_score - right_score), MAX_SCORE_DIFF)
	var bar_progress = log(score_diff + 1) / log(MAX_SCORE_DIFF + 1)
	rect_size = Vector2(size.x / 2, size.y / 4)
	fit_child_in_rect($ScoreBar1P, Rect2(Vector2(0, size.y * 5 / 8), rect_size))
	fit_child_in_rect($ScoreBar2P, Rect2(Vector2(size.x / 2, size.y * 5 / 8), rect_size))

	rect_size = Vector2(size.x / 2, size.y * 3 / 8)
	$Score1P/RichTextLabel.clear()
	$Score2P/RichTextLabel.clear()
	$ScoreDiff/RichTextLabel.clear()
	$Score1P/RichTextLabel.push_font_size(32)
	$Score2P/RichTextLabel.push_font_size(32)
	$ScoreDiff/RichTextLabel.push_font_size(16)
	if left_score > right_score:
		$ScoreBar1P.value = bar_progress
		$ScoreBar2P.value = 0
		$Score1P/RichTextLabel.push_bold()
		$Score1P/RichTextLabel.add_text("%d" % left_score)
		$Score1P/RichTextLabel.pop()
		$Score2P/RichTextLabel.add_text("%d" % right_score)
		$ScoreDiff/RichTextLabel.add_text("-%d" % score_diff)
		$ScoreDiff/RichTextLabel.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
		fit_child_in_rect($ScoreDiff, Rect2(Vector2(size.x / 2, size.y * 4 / 8), rect_size))
	elif left_score == right_score:
		$ScoreBar1P.value = 0
		$ScoreBar2P.value = 0
		$Score1P/RichTextLabel.add_text("%d" % left_score)
		$Score2P/RichTextLabel.add_text("%d" % right_score)
	else:
		$ScoreBar2P.value = bar_progress
		$ScoreBar1P.value = 0
		$Score1P/RichTextLabel.add_text("%d" % left_score)
		$Score2P/RichTextLabel.push_bold()
		$Score2P/RichTextLabel.add_text("%d" % right_score)
		$Score2P/RichTextLabel.pop()
		$ScoreDiff/RichTextLabel.add_text("-%d" % score_diff)
		$ScoreDiff/RichTextLabel.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		fit_child_in_rect($ScoreDiff, Rect2(Vector2(0, size.y * 4 / 8), rect_size))
	$Score1P/RichTextLabel.pop()
	$Score2P/RichTextLabel.pop()
	$ScoreDiff/RichTextLabel.pop()
	rect_size = Vector2(size.x / 2, size.y * 5 / 8)
	fit_child_in_rect($Score1P, Rect2(Vector2(0, 0), rect_size))
	fit_child_in_rect($Score2P, Rect2(Vector2(size.x / 2, 0), rect_size))
