class_name WebAgent
extends Agent

enum CommandType {
	UNKNOWN = 0,
	GET_ALL_TERRAIN = 1,
	GET_SCORES = 2,
	GET_CURRENT_WAVE = 3,
	GET_REMAIN_TIME = 4,
	GET_TIME_UNTIL_NEXT_WAVE = 5,
	GET_MONEY = 6,
	GET_INCOME = 7,
	GET_GAME_STATUS = 8,
	GET_TERRAIN = 9,
	GET_SYSTEM_PATH = 10,
	GET_OPPONENT_PATH = 11,
	PLACE_TOWER = 101,
	GET_ALL_TOWERS = 102,
	GET_TOWER = 103,
	SELL_TOWER = 104,
	SET_STRATEGY = 105,
	SPAWN_UNIT = 201,
	GET_UNIT_COOLDOWN = 202,
	GET_ALL_ENEMIES = 203,
	CAST_SPELL = 301,
	GET_SPELL_COOLDOWN = 302,
	SEND_CHAT = 401,
	GET_CHAT_HISTORY = 402,
	SET_CHAT_NAME_COLOR = 403,
	PIXELCAT = 501,
	GET_DEVS = 502,
	SET_NAME = 503,
	DISCONNECT = 601,
	NTU_STUDENT_ID_CARD = 602,
	METAL_PIPE = 603,
	SPAM = 604,
	SUPER_STAR = 605,
	TURBO_ON = 606
}

const MAX_LOGGING_REQUEST = 100


class CommandHandler:
	var command_id: CommandType = CommandType.UNKNOWN
	var _arg_types: Array[Variant.Type]
	var _handler: Callable

	func _init(_command_id: CommandType, arg_types: Array[Variant.Type], handler: Callable) -> void:
		command_id = _command_id
		_arg_types = arg_types
		_handler = handler

	func check_argument_types(args: Variant) -> bool:
		if typeof(args) != TYPE_ARRAY:
			return false
		if args.size() != _arg_types.size():
			return false
		for i in range(_arg_types.size()):
			if typeof(args[i]) != _arg_types[i]:
				return false
		return true

	func handle(args: Array) -> Variant:
		return _handler.callv(args)


const MIN_COMMAND_INTERVAL_MSEC = 5
var _ws: WebSocketConnection = null
var _agent_identifier: String = ""
var _last_command: float = -1
# command id -> command handler
var _command_handlers: Dictionary = {}
# the set of command types that may be called when the game is not running
var _general_commands: Dictionary = {CommandType.GET_GAME_STATUS: null}
# the API quota reduction of each premium API
var _premium_commands: Dictionary = {
	CommandType.DISCONNECT: 1,
	CommandType.NTU_STUDENT_ID_CARD: 1,
	CommandType.METAL_PIPE: 1,
	CommandType.SPAM: 1,
	CommandType.SUPER_STAR: 1,
	CommandType.TURBO_ON: 1,
}


func _register_command_handlers() -> void:
	var handlers: Array[CommandHandler] = [
		CommandHandler.new(CommandType.GET_ALL_TERRAIN, [], _get_all_terrain),
		CommandHandler.new(CommandType.GET_TERRAIN, [TYPE_VECTOR2I], _get_terrain),
		CommandHandler.new(CommandType.GET_SCORES, [TYPE_BOOL], _get_scores),
		CommandHandler.new(CommandType.GET_CURRENT_WAVE, [], _get_current_wave),
		CommandHandler.new(CommandType.GET_REMAIN_TIME, [], _get_remain_time),
		CommandHandler.new(CommandType.GET_TIME_UNTIL_NEXT_WAVE, [], _get_time_until_next_wave),
		CommandHandler.new(CommandType.GET_MONEY, [TYPE_BOOL], _get_money),
		CommandHandler.new(CommandType.GET_INCOME, [TYPE_BOOL], _get_income),
		CommandHandler.new(CommandType.GET_GAME_STATUS, [], _get_game_status),
		CommandHandler.new(CommandType.GET_SYSTEM_PATH, [TYPE_BOOL], _get_system_path),
		CommandHandler.new(CommandType.GET_OPPONENT_PATH, [TYPE_BOOL], _get_opponent_path),
		CommandHandler.new(
			CommandType.PLACE_TOWER, [TYPE_INT, TYPE_STRING, TYPE_VECTOR2I], _place_tower
		),
		CommandHandler.new(CommandType.GET_ALL_TOWERS, [TYPE_BOOL], _get_all_towers),
		CommandHandler.new(CommandType.GET_TOWER, [TYPE_BOOL, TYPE_VECTOR2I], _get_tower),
		CommandHandler.new(CommandType.SELL_TOWER, [TYPE_VECTOR2I], _sell_tower),
		CommandHandler.new(CommandType.SET_STRATEGY, [TYPE_VECTOR2I, TYPE_INT], _set_strategy),
		CommandHandler.new(CommandType.SPAWN_UNIT, [TYPE_INT], _spawn_unit),
		CommandHandler.new(CommandType.GET_UNIT_COOLDOWN, [TYPE_INT], _get_unit_cooldown),
		CommandHandler.new(CommandType.GET_ALL_ENEMIES, [TYPE_BOOL], _get_all_enemies),
		CommandHandler.new(CommandType.CAST_SPELL, [TYPE_INT, TYPE_VECTOR2I], _cast_spell),
		CommandHandler.new(
			CommandType.GET_SPELL_COOLDOWN, [TYPE_BOOL, TYPE_INT], _get_spell_cooldown
		),
		CommandHandler.new(CommandType.SEND_CHAT, [TYPE_STRING], _send_chat),
		CommandHandler.new(CommandType.GET_CHAT_HISTORY, [TYPE_INT], _get_chat_history),
		CommandHandler.new(CommandType.SET_CHAT_NAME_COLOR, [TYPE_STRING], _set_chat_name_color),
		CommandHandler.new(CommandType.SET_NAME, [TYPE_STRING], _set_name),
		CommandHandler.new(CommandType.PIXELCAT, [], _pixel_cat),
		CommandHandler.new(CommandType.DISCONNECT, [], _disconnect),
		CommandHandler.new(CommandType.NTU_STUDENT_ID_CARD, [], _ntu_student_id_card),
		CommandHandler.new(CommandType.METAL_PIPE, [], _metal_pipe),
		CommandHandler.new(CommandType.SPAM, [TYPE_STRING], _spam),
		CommandHandler.new(CommandType.SUPER_STAR, [], _super_star),
		CommandHandler.new(CommandType.TURBO_ON, [], _turbo_on),
	]
	for handler in handlers:
		if _command_handlers.has(handler.command_id):
			pass  # error: duplicated handler id
		_command_handlers[handler.command_id] = handler


func _init() -> void:
	_register_command_handlers()
	_ws = ApiServer.register_connection()
	add_child(_ws)
	_ws.received_bytes.connect(_on_received_command)
	_ws.client_connected.connect(
		func():
			print("[API Server] WebAgent %s: Remote agent %s connected" % [_agent_identifier, name])
	)
	_ws.client_disconnected.connect(
		func():
			print(
				"[API Server] WebAgent %s: Remote agent %s disconnected" % [_agent_identifier, name]
			)
	)
	# keep processing requests when the game is paused
	process_mode = Node.PROCESS_MODE_ALWAYS


func _on_received_command(command_bytes: PackedByteArray) -> void:
	if game_self != null:
		game_self.api_called += 1
	# rate-limit commands
	var this_command = Time.get_ticks_msec()
	if _last_command >= 0 and this_command - _last_command < MIN_COMMAND_INTERVAL_MSEC:
		_ws.send_bytes(var_to_bytes([0, StatusCode.TOO_FREQUENT]))
		return
	_last_command = this_command

	# handle command
	var response: Array
	var command = bytes_to_var(command_bytes)
	if (
		typeof(command) != TYPE_ARRAY
		or command.size() < 2
		or typeof(command[0]) != TYPE_INT
		or typeof(command[1]) != TYPE_INT
	):
		response = [0, StatusCode.ILLFORMED_COMMAND]
	else:
		var request_id: int = command.pop_front()
		var command_id: int = command.pop_front()
		if request_id <= MAX_LOGGING_REQUEST:
			var command_name = (
				_command_handlers.get(command_id)._handler.get_method()
				if _command_handlers.has(command_id)
				else "(invalid)"
			)
			print(
				(
					"[API Server] WebAgent %s received command: %d, %d (%s)"
					% [_agent_identifier, request_id, command_id, command_name]
				)
			)
		elif request_id == MAX_LOGGING_REQUEST + 1:
			print(
				(
					"[API Server] WebAgent %s received more than %d requests, no further log will be printed."
					% [_agent_identifier, MAX_LOGGING_REQUEST]
				)
			)

		if not _command_handlers.has(command_id):
			response = [
				request_id,
				StatusCode.NOT_FOUND,
				"[Receive Command] Error: cannot find command: %d" % command_id
			]
		elif not _command_handlers[command_id].check_argument_types(command):
			response = [
				request_id, StatusCode.ILLEGAL_ARGUMENT, "[Receive Command] Error: illegal argument"
			]
		elif not game_running and not _general_commands.has(command_id):
			response = [
				request_id,
				StatusCode.NOT_STARTED,
				"[Receive Command] Error: the game is not running"
			]
		elif game_running and get_tree().paused and not _general_commands.has(command_id):
			response = [
				request_id, StatusCode.PAUSED, "[Receive Command] Error: the game is paused"
			]
		elif (
			_premium_commands.has(command_id)
			and game_self.premium_api_quota < _premium_commands[command_id]
		):
			response = [
				request_id,
				StatusCode.INSUFFICIENT_QUOTA,
				(
					"[Receive Command] Error: insufficient premium API quota. Required %d, but %d left"
					% [_premium_commands[command_id], game_self.premium_api_quota]
				)
			]
		else:
			if _premium_commands.has(command_id):
				game_self.premium_api_quota -= _premium_commands[command_id]
			response = _command_handlers[command_id].handle(command)
			if game_self != null:
				game_self.api_succeed += (response[0] == StatusCode.OK) as int
			response.push_front(request_id)

	_ws.send_bytes(var_to_bytes(response))
