extends CharacterBody2D

@export var speed := 100.0
var path_follow: PathFollow2D


func _ready():
	path_follow = get_parent() as PathFollow2D


func _process(delta):
	path_follow.progress += speed * delta
	if path_follow.progress_ratio >= 1.0:
		queue_free()
