extends Control

var screen_size := Vector2.ZERO
var velocity := Vector2(400, 300)
var match_score: int = 0
var understand_time: int = 3

@onready var logo := $Subtitle
@onready var distros := [
	preload("res://ui/distro/arch.tscn"),
	preload("res://ui/distro/debian.tscn"),
	preload("res://ui/distro/fedora.tscn"),
	preload("res://ui/distro/freebsd.tscn"),
	preload("res://ui/distro/macos.tscn"),
	preload("res://ui/distro/manjaro.tscn"),
	preload("res://ui/distro/nixos.tscn"),
	preload("res://ui/distro/ubuntu.tscn"),
	preload("res://ui/distro/windows.tscn")
]


func _ready() -> void:
	screen_size = get_viewport_rect().size
	_change_color()
	logo.position = Vector2(
		randf_range(0, screen_size.x - logo.get_minimum_size().x),
		randf_range(0, screen_size.y - logo.get_minimum_size().y)
	)

	var config: ConfigFile = ConfigFile.new()
	var current_time = Time.get_datetime_dict_from_system()
	if current_time["month"] == 7 and current_time["day"] == 18 and current_time["hour"] in 1:
		config.set_value("Time", "Warning", true)
	if config.get_value("Time", "Warning", false) == true:
		$Warning.visible = true

	if not AudioManager.background_menu.has_stream_playback():
		AudioManager.background_menu.play()
	$VersionMargin/Version/Version.text = (
		"v%s" % [ProjectSettings.get_setting("application/config/version")]
	)


func _on_understand_pressed() -> void:
	if randi_range(0, 3) == 0:
		understand_time = 0
	if understand_time == 3:
		$Warning/Start.text = "Are you sure"
		if randi_range(0, 3) == 0:
			understand_time = 0
	elif understand_time == 2:
		$Warning/Start.text = "Are you really sure"
	elif understand_time == 1:
		$Warning/Start.text = "Are you really really sure"
	elif understand_time == 0:
		$Warning.visible = false
	understand_time -= 1


func _on_start_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/player_selection/player_selection.tscn")


func _on_quad_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/quad/quad_match_loader.tscn")


func _on_about_pressed() -> void:
	AudioManager.button_on_click.play()
	get_tree().change_scene_to_file("res://scenes/about.tscn")


func _on_quit_pressed() -> void:
	get_tree().quit()


func _on_settings_pressed() -> void:
	$Settings.open()


func _on_changelog_pressed() -> void:
	OS.shell_open("https://github.com/CSIE-Challenge/Challenge2025/releases")


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

	if match_score > 0:
		var hundred: int = floori(match_score / 100.0)
		var ten: int = floori((match_score % 100) / 10.0)
		var one: int = match_score % 10
		$VersionMargin/Version/Version.text = "v%d.%d.%d" % [hundred, ten, one]
	if match_score >= 256:
		get_tree().change_scene_to_file("res://scenes/distro_intro.tscn")


func _change_color():
	logo.modulate = Color(randf(), randf(), randf())


func _on_timer_timeout() -> void:
	var d = distros.pick_random().instantiate()
	var screen_width = get_viewport_rect().size.x
	d.position = Vector2(randf_range(0, screen_width), -50)
	d.rotation = randf_range(0, TAU)
	d.set_script(load("res://ui/distro/distro.gd"))
	add_child(d)
