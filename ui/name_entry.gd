extends HBoxContainer

@export var dev_name: String
@export var link := ""


func _ready():
	$Name.text = dev_name
	if link != "":
		$LinkButton.text = link
	else:
		$LinkButton.hide()
