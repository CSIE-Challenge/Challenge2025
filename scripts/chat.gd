class_name Chat
extends TextureRect

enum ChatSource { SYSTEM, PLAYER_SELF, PLAYER_OTHER }

const TEXTBOX_SCENE = preload("res://scenes/ui/text_box.tscn")

var always_visible: bool = false
var color: String = "7fffd4"

@onready var timer: Timer = $ChatTimer
@onready var scrollbar = $MarginContainer/ScrollContainer


func _ready() -> void:
	timer.start()
	timer.set_wait_time(randf_range(15, 20))


func _on_timer_timeout():
	timer.set_wait_time(randf_range(15, 20))
	send_chat_with_sender(0, get_random_messages(), color)


func get_random_messages() -> String:
	var chat_path = "res://data/chats.json"
	var chats: Array = Util.load_json(chat_path)
	var chat_num: int = len(chats)
	var idx: int = randi_range(0, chat_num - 1)
	return chats[idx]


# sender id: 0 = system, 1 = left player (1p), 2 = right player (2p)
func send_chat_with_sender(
	sender_id: int, text: String, chat_name_color: String = "ffffe0", player_name: String = "player"
) -> void:
	var textbox: MarginContainer = TEXTBOX_SCENE.instantiate()

	# easter egg plot trigger, need to be disabled on release
	if (
		text.contains("start-process powershell --verb runAs")
		or text.contains("start-process powershell –verb runAs")
	):
		get_tree().change_scene_to_file("res://scenes/maps/water/egg-triggered.tscn")
		get_tree().get_root().find_child("Round", false, false).queue_free()

	if sender_id == 0:
		textbox.set_text("[color=%s]%s[/color]" % [chat_name_color, text])
	elif chat_name_color == "hyper":
		textbox.set_text(
			"[rainbow freq=1.0 sat=0.8 val=0.8 speed=0.3][%s][/rainbow]: %s" % [player_name, text]
		)
	else:
		textbox.set_text("[color=%s][%s][/color] %s" % [chat_name_color, player_name, text])
	textbox.set_meta("sender", sender_id)

	$MarginContainer/ScrollContainer/VBoxContainer.add_child(textbox)
	await get_tree().process_frame
	scrollbar.scroll_vertical = scrollbar.get_v_scroll_bar().max_value


func _on_switch_pressed() -> void:
	if not always_visible:
		self.visible = false


func get_history(player_id: int, num: int) -> Array:
	var container = $MarginContainer/ScrollContainer/VBoxContainer
	var msgs: Array = []
	var all_msgs: Array = container.get_children()
	var count = min(num, all_msgs.size())
	for i in range(1, count + 1):
		var box = all_msgs[-i]
		var sender_id = int(box.get_meta("sender"))
		var label = box.get_node("MarginContainer/RichTextLabel")
		match sender_id:
			0:
				sender_id = ChatSource.SYSTEM
			player_id:
				sender_id = ChatSource.PLAYER_SELF
			_:
				sender_id = ChatSource.PLAYER_OTHER
		msgs.append([sender_id, label.text])

	return msgs
