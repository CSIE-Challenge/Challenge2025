extends Control

var screen_size := Vector2.ZERO
var velocity := Vector2(400, 300)
var match_score: int = 0
var understand_time = 4
var won_in_distro = false

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
	print("HYJO{>:tPU;8fHHh<[:9}")
	screen_size = get_viewport_rect().size
	$VBoxContainer/Quit.grab_focus()
	_change_color()
	logo.position = Vector2(
		randf_range(0, screen_size.x - logo.get_minimum_size().x),
		randf_range(0, screen_size.y - logo.get_minimum_size().y)
	)

	var config: ConfigFile = ConfigFile.new()
	var current_time = Time.get_datetime_dict_from_system()
	if (
		current_time["month"] == 7
		and current_time["day"] == 18
		and current_time["hour"] in [3, 4, 5]
	):
		config.set_value("Time", "Warning", true)
	if config.get_value("Time", "Warning", false) == true and !OS.has_feature("editor"):
		$Warning.visible = true

	if not AudioManager.background_menu.has_stream_playback():
		AudioManager.background_menu.play()
	$VersionMargin/Version/Version.text = (
		"v%s" % [ProjectSettings.get_setting("application/config/version")]
	)


func _on_understand_pressed() -> void:
	if randi_range(0, 3) == 0:
		understand_time = 0

	if understand_time == 4:
		$Warning/Start.text = "Are you sure?"
		if randi_range(0, 3) == 0:
			understand_time = 0
	elif understand_time == 3:
		$Warning/Start.text = "Are you really sure?"
	elif understand_time == 2:
		$Warning/Start.text = "Are you really really sure?"
	elif understand_time == 1:
		$Warning/Start.text = "Are you genuinely sure?"
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
	AudioManager.button_on_click.play()
	$Settings.open()


func _on_changelog_pressed() -> void:
	OS.shell_open("https://github.com/CSIE-Challenge/Challenge2025/releases")


func _on_hidden_pressed() -> void:
	var pwd = $Hahayoufoundit.text
	var line = ""
	for c in [104, 97, 72, 52, 95, 106, 48, 118, 95, 118, 48, 118, 73, 55, 100, 95, 49, 55]:
		line += char(c)
	$Hahayoufoundit.text = "ARCH{" + line + "}"
	$Hahayoufoundit.set_visible(true)


func _seven() -> void:
	var result = ""
	for c in [
		0x4f60,
		0x6839,
		0x672c,
		0x662f,
		0x0020,
		0x0037,
		0x0078,
		0x0020,
		0x51a0,
		0x8ecd,
		0xff0c,
		0x5c45,
		0x7136,
		0x80fd,
		0x7a81,
		0x7834,
		0x0020,
		0x0037,
		0x0037,
		0x0034,
		0x0039,
		0x0020,
		0x7684,
		0x969c,
		0x7919,
		0xff01,
		0x4ee5,
		0x4e0b,
		0x662f,
		0x4f60,
		0x7684,
		0x734e,
		0x52f5,
		0xff1a,
		0x0041,
		0x0052,
		0x0043,
		0x0048,
		0x007b,
		0x0071,
		0x0075,
		0x006f,
		0x0074,
		0x0065,
		0x005f,
		0x0035,
		0x0033,
		0x0056,
		0x0033,
		0x004e,
		0x005f,
		0x0071,
		0x0075,
		0x006f,
		0x0074,
		0x0065,
		0x007d
	]:
		result += char(c)
	$seven.text = result
	$seven.visible = true


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
	if match_score >= 256 and not won_in_distro:
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
