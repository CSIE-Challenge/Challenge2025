class_name IndividualPlayerSelection
extends Panel

signal manual_control_enabled

@export var player_identifier: String = "Player 1"

var manual_control: bool = false
var python_subprocess: PythonSubprocessManager
var web_agent: WebAgent

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

	# agent script
	agent_script_button.pressed.connect(agent_script_dialog.popup)
	agent_script_dialog.file_selected.connect(python_subprocess.set_python_script)

	# process status
	process_status_run_button.pressed.connect(python_subprocess.run_subprocess)
	process_status_kill_button.pressed.connect(python_subprocess.kill_subprocess)

	# token
	var the_token = web_agent._ws._token
	$Options/TokenLabel.text = the_token
	$Options/TokenContainer/Button.pressed.connect(
		func():
			DisplayServer.clipboard_set(the_token)
			$Options/TokenContainer/Button.text = "Copied!"
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


func save_config(config: ConfigFile, section: String) -> void:
	config.set_value(section, "player_identifier", player_identifier)
	config.set_value(section, "manual_control", manual_control)
	config.set_value(section, "python_interpreter", python_subprocess.python_interpreter_path)
	config.set_value(section, "agent_script", python_subprocess.python_script_path)


func _remove_handlers(sig: Signal) -> void:
	var conns = sig.get_connections()
	for iter in conns:
		sig.disconnect(iter["callable"])


func freeze() -> void:
	_remove_handlers(manual_control_off_button.pressed)
	_remove_handlers(manual_control_on_button.pressed)


func _display_fields() -> void:
	# manual control
	manual_control_off_button.visible = not manual_control
	manual_control_on_button.visible = manual_control

	# python interpreter
	var python_interpreter_path = python_subprocess.python_interpreter_path
	if not python_interpreter_path.is_empty():
		python_interpreter_label.text = python_interpreter_path
	else:
		python_interpreter_label.text = "(empty)"

	# agent script
	var agent_script_path = python_subprocess.python_script_path
	if not agent_script_path.is_empty():
		agent_script_label.text = agent_script_path
	else:
		agent_script_label.text = "(empty)"

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
