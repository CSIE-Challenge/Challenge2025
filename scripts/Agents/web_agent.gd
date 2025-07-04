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
	var id: CommandType
	var _arg_types: Array[Variant.Type]
	var _handler: Callable

	func _init(command_id: int, arg_types: Array[Variant.Type], handler: Callable) -> void:
		id = command_id
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


const MIN_COMMAND_INTERVAL_MSEC = 10
var _ws: WebSocketConnection = null
var _last_command: float = -1
var _command_handlers: Dictionary = {}  # command id -> command handler


func _register_command_handlers() -> void:
	var handlers: Array[CommandHandler] = [
		CommandHandler.new(CommandType.GET_ALL_TERRAIN, [TYPE_VECTOR2I, TYPE_INT], build),
		# TODO
	]
	for handler in handlers:
		if _command_handlers.has(handler.id):
			pass  # error: duplicated handler id
		_command_handlers[handler.id] = handler


func _init() -> void:
	type = AgentType.AI
	_register_command_handlers()


func link(ws: WebSocketConnection) -> void:
	_ws = ws
	_ws.received_bytes.connect(_on_received_command)


func _on_received_command(command_bytes: PackedByteArray) -> void:
	# rate-limit commands
	var this_command = Time.get_ticks_msec()
	if _last_command >= 0 and this_command - _last_command < MIN_COMMAND_INTERVAL_MSEC:
		return
	_last_command = this_command

	# handle command
	var response: Array
	var command = bytes_to_var(command_bytes)
	if (
		typeof(command) != TYPE_ARRAY
		or command.size() < 2
		or typeof(command[0]) != TYPE_PACKED_BYTE_ARRAY
		or typeof(command[1]) != TYPE_INT
	):
		response.push_back(StatusCode.ILLFORMED_COMMAND)
	else:
		var command_id: int = command.pop_front()
		if not _command_handlers.has(command_id):
			response.push_back(StatusCode.NOT_FOUND)
		elif not _command_handlers[command_id].check_argument_types(command):
			response.push_back(StatusCode.ILLEGAL_ARGUMENT)
		else:
			response = _command_handlers[command_id].handle(command)

	_ws.send_bytes(var_to_bytes(response))
