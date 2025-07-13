class_name PythonSubprocessManager
extends Node

enum { NEVER_RUN, RUNNING, KILLED, EXITED, FAILED }

@export var python_interpreter_path: String = ""
@export var python_script_path: String = ""

var _state: int = NEVER_RUN
var _current_pid: int
var _current_stdio_pipe: FileAccess
var _last_exit_code: int


func _init() -> void:
	OS.set_environment("IS_CHALLENGE_GAME_PROCESS", "TRUE")
	# keep monitoring the subprocess when the game is paused
	process_mode = Node.PROCESS_MODE_ALWAYS


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
	_current_pid = OS.create_process(python_interpreter_path, [python_script_path])
	if _current_pid == -1:
		_state = FAILED
		return
	_state = RUNNING


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


func _exit_tree() -> void:
	kill_subprocess()


func _notification(what):
	if what == NOTIFICATION_PREDELETE:
		self.kill_subprocess()
