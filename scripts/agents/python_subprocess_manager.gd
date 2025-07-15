class_name PythonSubprocessManager
extends Node

enum { NEVER_RUN, RUNNING, KILLED, EXITED, FAILED }

# waiting time from this termination to next auto-restart
const RESTART_INTERVAL_SEC: float = 1.0

@export var python_interpreter_path: String = ""
@export var python_script_path: String = ""
@export var auto_restart: bool = false

var _state: int = NEVER_RUN
var _current_pid: int
var _current_stdio_pipe: FileAccess
var _last_exit_code: int
var _restart_timer: Timer
var _ran_after_setting_auto_restart: bool = false


func _init() -> void:
	_restart_timer = Timer.new()
	add_child(_restart_timer)
	_restart_timer.one_shot = true
	_restart_timer.wait_time = RESTART_INTERVAL_SEC
	_restart_timer.timeout.connect(run_subprocess)

	OS.set_environment("IS_CHALLENGE_GAME_PROCESS", "TRUE")
	# keep monitoring the subprocess when the game is paused
	process_mode = Node.PROCESS_MODE_ALWAYS


func set_python_interpreter(path: String) -> void:
	python_interpreter_path = path


func set_python_script(path: String) -> void:
	python_script_path = path


func set_auto_restart(value: bool) -> void:
	auto_restart = value
	if not auto_restart:
		_restart_timer.stop()
		_ran_after_setting_auto_restart = false


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


func is_restarting() -> bool:
	return not _restart_timer.is_stopped()


# start the subprocess and send the token via stdin
func run_subprocess() -> void:
	if not is_runnable():
		return
	_restart_timer.stop()
	_current_pid = OS.create_process(python_interpreter_path, [python_script_path])
	if _current_pid == -1:
		_state = FAILED
		return
	_state = RUNNING


# terminate the subprocess
func kill_subprocess() -> void:
	set_auto_restart(false)
	_restart_timer.stop()
	if not is_running():
		return
	_state = KILLED
	OS.kill(_current_pid)


func _process(_delta: float) -> void:
	if _state != RUNNING and _state != KILLED:
		# process is not running and is not killed, possibly runnable
		if _ran_after_setting_auto_restart and auto_restart and not is_restarting():
			_restart_timer.start()
		return
	if OS.is_process_running(_current_pid):
		if auto_restart:
			_ran_after_setting_auto_restart = true
		# close the stdio pipes once we get responses from stdout pipe
		if _current_stdio_pipe != null and _current_stdio_pipe.get_length() > 0:
			_current_stdio_pipe = null
		return
	# collect exit code if the subprocess has terminated
	_state = EXITED
	_last_exit_code = OS.get_process_exit_code(_current_pid)


func _notification(what):
	if what == NOTIFICATION_PREDELETE:
		kill_subprocess()
