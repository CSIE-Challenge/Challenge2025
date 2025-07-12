class_name EndPlayerStats
extends MarginContainer


func set_stat(name: String, score: int, kill_count: int, money: int):
	$Box/Name.text = name
	$Box/MarginContainer/GridContainer/Score.text = "%d" % score
	$Box/MarginContainer/GridContainer/Kill.text = "%d" % kill_count
	$Box/MarginContainer/GridContainer/Money.text = "%d" % money
