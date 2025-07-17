extends Node2D

enum DistroType { ARCH, DEBIAN, FEDORA, FREEBSD, MACOS, MANJARO, NIXOS, UBUNTU, WINDOWS }
@export var distro_type: DistroType

var surrounded_distro: Array


func _ready() -> void:
	$Match.connect("body_entered", _on_body_entered)
	$Match.connect("body_exited", _on_body_exited)
	$Click.connect("input_event", _on_input_event)


func _process(_delta):
	if position.y > get_viewport_rect().size.y + 50:
		queue_free()


func _on_body_entered(body) -> void:
	if "distro_type" in body and body.distro_type == distro_type:
		surrounded_distro.push_back(body)


func _on_body_exited(body) -> void:
	if "distro_type" in body and body.distro_type == distro_type:
		surrounded_distro.erase(body)


func _play_match_sound() -> void:
	if distro_type == DistroType.MACOS:
		AudioManager.macos.play()
	elif distro_type == DistroType.WINDOWS:
		AudioManager.windows.play()
	else:
		AudioManager.match_sound.play()


func _on_input_event(_viewport, event: InputEvent, _shape_idx) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if surrounded_distro.size() >= 2:
			_play_match_sound()
			if surrounded_distro.size() >= 7:
				get_parent()._seven()
			get_parent().match_score += pow(surrounded_distro.size(), 2)
			for distro in surrounded_distro:
				distro.queue_free()
