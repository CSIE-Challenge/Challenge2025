extends Control

@export var plot_text: String = """> start-process powershell --verb runAs
Privilege elevated.
> shutdown /r /fw
Booting into UEFI...
Booted into UEFI.
Installing Arch Linux...

Thank you for your support of open-source software.
Your unmatched intelligence moved the world toward a more open, freer place.
Thanks to you, our true hero!
You may record this as your certificate of such conviction.
"""

@export var credit_text: String = """
CSIE Camp Challenge 2025 超 解碼 農兄弟
Thanks for your playing!

Project Management & Quality Assurance
	胡祐誠 HyperSoWeak 邱翊均 PixelCat
Game Design & Game Programming
	卓育安 prairie2022 常洧丞 Weber Change 廖禹喬 JoyLiao 張聲元 LightningFarter 李尚哲 Matt 林文繡 bbwinner
	洪德朗 Andromeda 王　淇 littlecube8152 胡祐誠 HyperSoWeak 蔡孟憬 cmj 蔡孟衡 lemonilemon 蔡瑜恩 Jaime 邱翊均 PixelCat
Art
	張嘉泰 TDDY 張聲元 LightningFarter 胡祐誠 HyperSoWeak 謝承憲 ChengHsien
Music & Sound Effect
	李尚哲 Matt 林文繡 bbwinner
Agent Design & Game Testing
	張聲元 LightningFarter 李尚哲 Matt 蔡瑜恩 Jaime

Special Thanks
	Challenge 2024 開發團隊
	主辦　資工系系學會
	一起籌備資訊營的人們與參加資訊營的所有人


Press any key to continue...
"""

@export var second_per_plot_character = 0.1
@export var second_pause_per_plot_line = 1
@export var second_per_credit_character = 0.025
@export var second_pause_per_credit_line = 0.5

var is_animation_finished = false


func _ready():
	create_animation()
	$AnimationPlayer.play("text-reveal")
	if AudioManager.second_stage:
		AudioManager.background_game_stage2.stop()
	else:
		AudioManager.background_game_stage1.stop()


func _on_bgm_timer_timeout():
	AudioManager.background_menu.play()


func create_animation():
	var animation: Animation = $AnimationPlayer.get_animation("text-reveal")
	animation.clear()

	var track_idx = animation.add_track(Animation.TYPE_VALUE)
	animation.track_set_path(track_idx, "Centering/RichTextLabel:text")
	animation.track_set_interpolation_type(track_idx, Animation.INTERPOLATION_LINEAR)
	animation.value_track_set_update_mode(track_idx, Animation.UPDATE_CONTINUOUS)

	var plot_lines = plot_text.split("\n")
	var credit_lines = credit_text.split("\n")
	var current_time = 0
	var current_text = ""

	animation.track_insert_key(track_idx, current_time, current_text)
	for line in plot_lines:
		if line.length() >= 16 and line[5] == "s" and line[15] == "o":
			line = "                "
			for c in [
				65,
				82,
				67,
				72,
				123,
				53,
				85,
				112,
				101,
				114,
				95,
				68,
				51,
				99,
				79,
				100,
				69,
				114,
				95,
				70,
				52,
				114,
				77,
				51,
				114,
				95,
				56,
				114,
				111,
				53,
				125
			]:
				line += char(c)
		current_text += line + "\n"
		current_time += second_per_plot_character * (line.length())
		animation.track_insert_key(track_idx, current_time, current_text)
		current_time += second_pause_per_plot_line
		animation.track_insert_key(track_idx, current_time, current_text)
	$BGMTimer.wait_time = current_time
	$BGMTimer.start()
	for line in credit_lines:
		current_text += line + "\n"
		current_time += second_per_credit_character * (line.length())
		animation.track_insert_key(track_idx, current_time, current_text)
		current_time += second_pause_per_credit_line
		animation.track_insert_key(track_idx, current_time, current_text)
	animation.set_length(current_time)


func _input(event):
	if event is InputEventKey and event.pressed and is_animation_finished:
		OS.shell_open("https://wiki.archlinux.org/title/Installation_guide")
		get_tree().quit()


func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	if anim_name == "text-reveal":
		is_animation_finished = true
