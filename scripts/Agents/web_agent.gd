class_name WebAgent
extends Agent

enum CommandType { BUILD, SELL, UPGRADE, USE_SKILL, GET_MAP, GET_PLAYER_STATE, GET_OPPONENT_STATE }
enum CommandReturnCode {
	OK,
	ERR_ILLFORMED_COMMAND,
	ERR_DOES_NOT_EXIST,
	ERR_ILLEGAL_ARG_TYPES,
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


const MIN_COMMAND_INTERVAL_MSEC = 5
var _ws: WebSocketConnection = null
var _last_command: float = -1
var _command_handlers: Dictionary = {}  # command id -> command handler


func _register_command_handlers() -> void:
	var handlers: Array[CommandHandler] = [
		CommandHandler.new(CommandType.BUILD, [TYPE_VECTOR2I, TYPE_INT], build),
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
	var ret_code: Variant
	var ret_value: Variant = null
	var command = bytes_to_var(command_bytes)
	if typeof(command) != TYPE_ARRAY or command.size() < 1 or typeof(command[0]) != TYPE_INT:
		ret_code = CommandReturnCode.ERR_ILLFORMED_COMMAND
	else:
		var command_id: int = command.pop_front()
		if not _command_handlers.has(command_id):
			ret_code = CommandReturnCode.ERR_DOES_NOT_EXIST
		elif not _command_handlers[command_id].check_argument_types(command):
			ret_code = CommandReturnCode.ERR_ILLEGAL_ARG_TYPES
		else:
			ret_code = CommandReturnCode.OK
			ret_value = _command_handlers[command_id].handle(command)

	# write return values back to websocket
	if typeof(ret_value) != TYPE_ARRAY:
		ret_value = [ret_value]
	ret_value.push_front(ret_code)
	_ws.send_bytes(var_to_bytes(ret_value))
