class_name APIServer
extends Node

#region Server singleton
static var _instance: APIServer = null


static func get_instance() -> APIServer:
	return _instance


func _ready() -> void:
	pass
#endregion
