class_name IndividualPlayerSelection
extends Panel

signal manual_control_enabled

@export var player_identifier: String = "Player 1"

var manual_control: bool = false
var python_subprocess: PythonSubprocessManager
var web_agent: WebAgent
var _update_paths: bool = true

@onready var manual_control_on_button: Button = $Options/ManualControlContainer/ButtonOn
@onready var manual_control_off_button: Button = $Options/ManualControlContainer/ButtonOff
@onready var python_interpreter_label: Label = $Options/PythonInterpreterLabel
@onready var python_interpreter_button: Button = $Options/PythonInterpreterContainer/Button
@onready var python_interpreter_dialog: FileDialog = $Options/PythonInterpreterContainer/FileDialog
@onready var agent_script_label: Label = $Options/AgentScriptLabel
@onready var agent_script_button: Button = $Options/AgentScriptContainer/Button
@onready var agent_script_dialog: FileDialog = $Options/AgentScriptContainer/FileDialog
@onready var process_status_container: HBoxContainer = $Options/ProcessStatusContainer
@onready var process_status_run_button: Button = $Options/ProcessStatusContainer/ButtonRun
@onready var process_status_kill_button: Button = $Options/ProcessStatusContainer/ButtonKill
@onready var process_status_label: Label = $Options/ProcessStatusLabel
@onready var token_copy_button: Button = $Options/TokenContainer/Button
@onready var token_copied_timer: Timer = $Options/TokenContainer/CopiedTextTimer
@onready var token_label: Label = $Options/TokenContentContainer/TokenLabel
@onready var agent_connected_label: Label = $Options/AgentStatusContainer/AgentStatusConnected
@onready var agent_disconnected_label: Label = $Options/AgentStatusContainer/AgentStatusDisconnected

#region Node Lifecycle


func _init() -> void:
	python_subprocess = PythonSubprocessManager.new()
	add_child(python_subprocess)
	web_agent = WebAgent.new()
	add_child(web_agent)


# Setting up signal handlers in _ready because I want to avoid having a large amount
# of individual one-line functions. Connect the handlers at runtime with anonymous
# lambda functions could be more concise.
func _ready() -> void:
	$PlayerIdentifierLabel.text = player_identifier

	# manual control
	manual_control_off_button.pressed.connect(
		func():
			manual_control = true
			manual_control_enabled.emit()
	)
	manual_control_on_button.pressed.connect(func(): manual_control = false)

	# python interpreter
	python_interpreter_button.pressed.connect(python_interpreter_dialog.popup)
	python_interpreter_dialog.file_selected.connect(python_subprocess.set_python_interpreter)
	python_interpreter_dialog.file_selected.connect(func(_path: String): _update_paths = true)

	# agent script
	agent_script_button.pressed.connect(agent_script_dialog.popup)
	agent_script_dialog.file_selected.connect(python_subprocess.set_python_script)
	agent_script_dialog.file_selected.connect(func(_path: String): _update_paths = true)

	# process status
	process_status_run_button.pressed.connect(python_subprocess.run_subprocess)
	process_status_kill_button.pressed.connect(python_subprocess.kill_subprocess)

	# token
	token_copied_timer.timeout.connect(func(): token_copy_button.text = "Copy")
	token_copy_button.pressed.connect(
		func():
			DisplayServer.clipboard_set(web_agent._ws._token)
			$Options/TokenContainer/Button.text = "Copied!"
			token_copied_timer.start()
	)
	$Options/TokenContentContainer/Button.pressed.connect(
		func(): ApiServer.update_token(web_agent._ws, ApiServer.generate_token())
	)

	# web agent status
	web_agent._ws.client_connected.connect(
		func():
			agent_connected_label.visible = true
			agent_disconnected_label.visible = false
	)
	web_agent._ws.client_disconnected.connect(
		func():
			agent_connected_label.visible = false
			agent_disconnected_label.visible = true
	)


func _process(_delta: float) -> void:
	_display_fields()


#endregion


func load_config(config: ConfigFile, section: String) -> void:
	player_identifier = config.get_value(section, "player_identifier", section)
	manual_control = config.get_value(section, "manual_control", false)
	python_subprocess.set_python_interpreter(config.get_value(section, "python_interpreter", ""))
	python_subprocess.set_python_script(config.get_value(section, "agent_script", ""))
	if config.has_section_key(section, "api_token"):
		ApiServer.update_token(web_agent._ws, config.get_value(section, "api_token"))


func save_config(config: ConfigFile, section: String) -> void:
	config.set_value(section, "player_identifier", player_identifier)
	config.set_value(section, "manual_control", manual_control)
	config.set_value(section, "python_interpreter", python_subprocess.python_interpreter_path)
	config.set_value(section, "agent_script", python_subprocess.python_script_path)
	config.set_value(section, "api_token", web_agent._ws._token)


func _remove_handlers(sig: Signal) -> void:
	var conns = sig.get_connections()
	for iter in conns:
		sig.disconnect(iter["callable"])


func freeze() -> void:
	_remove_handlers(manual_control_off_button.pressed)
	_remove_handlers(manual_control_on_button.pressed)


func _get_string_width(content: String) -> float:
	return (
		get_theme_default_font()
		. get_string_size(content, HORIZONTAL_ALIGNMENT_LEFT, -1, get_theme_default_font_size())
		. x
	)


func _truncate_front(content: String, max_width: float) -> String:
	if _get_string_width(content) < max_width:
		return content
	for i in range(len(content)):
		var truncated = "…" + content.substr(i)
		if _get_string_width(truncated) < max_width:
			return truncated
	return ""


func _display_fields() -> void:
	# manual control
	manual_control_off_button.visible = not manual_control
	manual_control_on_button.visible = manual_control

	if _update_paths:
		# python interpreter
		var python_interpreter_path = _truncate_front(
			python_subprocess.python_interpreter_path, python_interpreter_label.size.x
		)
		if not python_interpreter_path.is_empty():
			python_interpreter_label.text = python_interpreter_path
		else:
			python_interpreter_label.text = "(empty)"
		# agent script
		var agent_script_path = _truncate_front(
			python_subprocess.python_script_path, agent_script_label.size.x
		)
		if not agent_script_path.is_empty():
			agent_script_label.text = agent_script_path
		else:
			agent_script_label.text = "(empty)"

	# token
	token_label.text = web_agent._ws._token

	# process status
	process_status_run_button.visible = python_subprocess.is_runnable()
	process_status_kill_button.visible = python_subprocess.is_running()
	process_status_container.visible = (
		python_subprocess.get_state() != PythonSubprocessManager.NEVER_RUN
		or python_subprocess.is_runnable()
	)
	process_status_label.visible = (
		python_subprocess.get_state() != PythonSubprocessManager.NEVER_RUN
	)
	match python_subprocess.get_state():
		PythonSubprocessManager.RUNNING:
			process_status_label.text = "Running (%d)" % python_subprocess.get_pid()
		PythonSubprocessManager.KILLED:
			process_status_label.text = "Killing"
		PythonSubprocessManager.EXITED:
			process_status_label.text = "Terminated (%d)" % python_subprocess.get_exit_code()
		PythonSubprocessManager.FAILED:
			process_status_label.text = "Failed"
