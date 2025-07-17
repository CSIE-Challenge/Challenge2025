# This is a reduced version of IndividualPlayerSelection for automated quad match loading
# It holds an instance of IndividualPlayerSelection, which will be handed to Game. Everything
# it shows and every input it takes is read from or passed to that IndividualPlayerSelection.
# Every field except for the connection status is read-only after being initialized from
# a config dictionary.

extends Panel

var selector: IndividualPlayerSelection = null
var options: Dictionary = {}


func _ready() -> void:
	selector = (
		preload("res://scenes/player_selection/individual_player_selection.tscn").instantiate()
	)
	selector.visible = false
	add_child(selector)
	visible = false


func init(_options: Dictionary, python_interpreter_path: String) -> void:
	visible = true
	selector.python_subprocess.set_python_interpreter(python_interpreter_path)
	# auto-restart is set in quad_match_loader.gd `toggle_all_agents()`

	options = _options
	selector.player_identifier = options["name"]
	selector.web_agent._agent_identifier = options["name"]
	var token = options["token"]
	ApiServer.update_token(selector.web_agent._ws, token)
	# TODO: pass API quota to the game
	var agent_script = options["agent-script"]
	selector.python_subprocess.set_python_script(agent_script)


func _process(_delta: float) -> void:
	var connected = selector.web_agent._ws.is_client_connected()
	$Options/AgentStatusContainer/Connected.visible = connected
	$Options/AgentStatusContainer/Disconnected.visible = not connected
	$Options/ProcessStatusLabel.text = selector.process_status_label.text
	display_options()


# the width of AgentScriptLabel is hard-coded because it is tricky to get the right update order
func display_options() -> void:
	if options.is_empty():
		return
	$PlayerNameLabel.text = options["name"]
	$Options/AgentScriptLabel.text = Util.truncate_front(
		self, options["agent-script"], $Options/AgentScriptLabel.size.x
	)
	$Options/TokenContainer/Token.text = options["token"]
	$Options/ApiQuotaContainer/ApiQuota.text = "%d" % options["api-quota"]
