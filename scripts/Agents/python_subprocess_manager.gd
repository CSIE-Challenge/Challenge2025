class_name PythonSubprocessManager
extends Node

enum { NEVER_RUN, RUNNING, KILLED, EXITED, FAILED }

@export var python_interpreter_path: String = ""
@export var python_script_path: String = ""

var _state: int = NEVER_RUN
var _send_token: String
var _current_pid: int
var _current_stdio_pipe: FileAccess
var _last_exit_code: int


func _init(send_token: String) -> void:
	OS.set_environment("IS_CHALLENGE_GAME_PROCESS", "TRUE")
	_send_token = send_token + "\n"


func set_python_interpreter(path: String) -> void:
	python_interpreter_path = path


func set_python_script(path: String) -> void:
	python_script_path = path


func get_state() -> int:
	return _state


func get_pid() -> int:
	if _state != RUNNING:
		return -1
	return _current_pid


func get_exit_code() -> int:
	if _state != EXITED:
		return -1
	return _last_exit_code


func is_running() -> bool:
	return _state == RUNNING


func is_runnable() -> bool:
	return (
		_state != RUNNING
		and _state != KILLED
		and not python_interpreter_path.is_empty()
		and not python_script_path.is_empty()
	)


# start the subprocess and send the token via stdin
func run_subprocess() -> void:
	if not is_runnable():
		return
	var dict = OS.execute_with_pipe(python_interpreter_path, [python_script_path])
	if dict.is_empty():
		_state = FAILED
		return
	_state = RUNNING
	_current_pid = dict["pid"]
	_current_stdio_pipe = dict["stdio"]
	_current_stdio_pipe.store_buffer(_send_token.to_ascii_buffer())


# terminate the subprocess
func kill_subprocess() -> void:
	if not is_running():
		return
	_state = KILLED
	OS.kill(_current_pid)


# close the stdio pipes once we get responses from stdout pipe
# check if the subprocess exited and collect exit code
func _process(_delta: float) -> void:
	if _state != RUNNING and _state != KILLED:
		return
	if OS.is_process_running(_current_pid):
		if _current_stdio_pipe != null and _current_stdio_pipe.get_length() > 0:
			_current_stdio_pipe = null
		return
	_state = EXITED
	_last_exit_code = OS.get_process_exit_code(_current_pid)
