class_name WebAgent
extends Agent

enum CommandType {
	GET_ALL_TERRAIN = 1,
	GET_SCORES = 2,
	GET_CURRENT_WAVE = 3,
	GET_REMAIN_TIME = 4,
	GET_TIME_UNTIL_NEXT_WAVE = 5,
	GET_MONEY = 6,
	GET_INCOME = 7,
	PLACE_TOWER = 101,
	GET_ALL_TOWERS = 102,
	GET_TOWER = 103,
	SPAWN_ENEMY = 201,
	GET_ENEMY_COOLDOWN = 202,
	GET_ALL_ENEMY_INFO = 203,
	GET_AVAILABLE_ENEMIES = 204,
	GET_CLOSEST_ENEMIES = 205,
	GET_ENEMIES_IN_RANGE = 206,
	CAST_SPELL = 301,
	GET_SPELL_COOLDOWN = 302,
	GET_ALL_SPELL_COST = 303,
	GET_EFFECTIVE_SPELLS = 304,
	SEND_CHAT = 401,
	GET_CHAT_HISTORY = 402
}


class CommandHandler:
	var command_id: CommandType
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
var _last_command: float = -1
var _command_handlers: Dictionary = {}  # command id -> command handler


func _register_command_handlers() -> void:
	var handlers: Array[CommandHandler] = [
		CommandHandler.new(CommandType.GET_ALL_TERRAIN, [], _get_all_terrain),
		CommandHandler.new(CommandType.GET_SCORES, [TYPE_BOOL], _get_scores),
		CommandHandler.new(CommandType.GET_CURRENT_WAVE, [], _get_current_wave),
		CommandHandler.new(CommandType.GET_REMAIN_TIME, [], _get_remain_time),
		CommandHandler.new(CommandType.GET_TIME_UNTIL_NEXT_WAVE, [], _get_time_until_next_wave),
		CommandHandler.new(CommandType.GET_MONEY, [TYPE_BOOL], _get_money),
		CommandHandler.new(CommandType.GET_INCOME, [TYPE_BOOL], _get_income),
		CommandHandler.new(CommandType.PLACE_TOWER, [TYPE_INT, TYPE_VECTOR2I], _place_tower),
		CommandHandler.new(CommandType.GET_ALL_TOWERS, [TYPE_BOOL], _get_all_towers),
		CommandHandler.new(CommandType.GET_TOWER, [TYPE_VECTOR2I], _get_tower),
		CommandHandler.new(CommandType.SPAWN_ENEMY, [TYPE_INT], _spawn_enemy),
		CommandHandler.new(
			CommandType.GET_ENEMY_COOLDOWN, [TYPE_BOOL, TYPE_INT], _get_enemy_cooldown
		),
		CommandHandler.new(CommandType.GET_ALL_ENEMY_INFO, [], _get_all_enemy_info),
		CommandHandler.new(CommandType.GET_AVAILABLE_ENEMIES, [], _get_available_enemies),
		CommandHandler.new(
			CommandType.GET_CLOSEST_ENEMIES, [TYPE_VECTOR2I, TYPE_INT], _get_closest_enemies
		),
		CommandHandler.new(
			CommandType.GET_ENEMIES_IN_RANGE, [TYPE_VECTOR2I, TYPE_FLOAT], _get_enemies_in_range
		),
		CommandHandler.new(CommandType.CAST_SPELL, [TYPE_INT, TYPE_VECTOR2I], _cast_spell),
		CommandHandler.new(
			CommandType.GET_SPELL_COOLDOWN, [TYPE_BOOL, TYPE_INT], _get_spell_cooldown
		),
		CommandHandler.new(CommandType.GET_ALL_SPELL_COST, [], _get_all_spell_cost),
		CommandHandler.new(CommandType.GET_EFFECTIVE_SPELLS, [TYPE_BOOL], _get_effective_spells),
		CommandHandler.new(CommandType.SEND_CHAT, [TYPE_STRING], _send_chat),
		CommandHandler.new(CommandType.GET_CHAT_HISTORY, [TYPE_INT], _get_chat_history)
	]
	for handler in handlers:
		if _command_handlers.has(handler.command_id):
			pass  # error: duplicated handler id
		_command_handlers[handler.command_id] = handler


func _init() -> void:
	type = AgentType.AI
	_register_command_handlers()
	_ws = ApiServer.register_connection()
	_ws.received_bytes.connect(_on_received_command)
	_ws.client_connected.connect(func(): print("[API Server] Remote agent %s connected" % name))
	_ws.client_disconnected.connect(
		func(): print("[API Server] Remote agent %s disconnected" % name)
	)


func _exit_tree() -> void:
	ApiServer.remove_connection(_ws)


func _on_received_command(command_bytes: PackedByteArray) -> void:
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
		print("[API Server] received command: ", request_id, " ", command_id)
		if not _command_handlers.has(command_id):
			response = [
				request_id,
				StatusCode.NOT_FOUND,
				"[Receive Command] Error: cannot find command: %d" % command_id
			]
		elif not _command_handlers[command_id].check_argument_types(command):
			response = [
				request_id,
				StatusCode.ILLEGAL_ARGUMENT,
				"[Receive Command] Error: illegal argument"
			]
		else:
			response = _command_handlers[command_id].handle(command)
			response.push_front(request_id)

	_ws.send_bytes(var_to_bytes(response))
