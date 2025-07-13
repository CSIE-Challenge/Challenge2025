extends Control

var screen_size := Vector2.ZERO
var velocity := Vector2(400, 300)

@onready var logo := $Subtitle


func _ready() -> void:
	screen_size = get_viewport_rect().size
	_change_color()
	logo.position = Vector2(
		randf_range(0, screen_size.x - logo.get_minimum_size().x),
		randf_range(0, screen_size.y - logo.get_minimum_size().y)
	)

	AudioManager.background_menu.play()
	$Version.text = "v%s" % [ProjectSettings.get_setting("application/config/version")]


func _on_start_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/player_selection/player_selection.tscn")


func _on_about_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/about.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()


func _process(delta):
	logo.position += velocity * delta

	var logo_size = logo.get_minimum_size()

	if logo.position.x < 0 or logo.position.x + logo_size.x > screen_size.x:
		velocity.x *= -1
		logo.position.x = clamp(logo.position.x, 0, screen_size.x - logo_size.x)
		_change_color()

	if logo.position.y < 0 or logo.position.y + logo_size.y > screen_size.y:
		velocity.y *= -1
		logo.position.y = clamp(logo.position.y, 0, screen_size.y - logo_size.y)
		_change_color()


func _change_color():
	logo.modulate = Color(randf(), randf(), randf())
