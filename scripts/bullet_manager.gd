extends Node2D

@export var speed := 400.0
@export var rotation_speed := 3.0
@export var max_distance := 800.0
@export var damage := 3

# class Bullet:
# 	var target: Node2D = null
# 	var origin: Vector2
# 	var position := Vector2()
# 	var orientation := 0.0
# 	var area_rid: RID
# 	var ci_rid: RID
# 	var pending_removal: bool = false

# RenderingServer expects references to be kept around
var bullet_texture = preload(
	"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile297.png"
)
var shape = preload("res://assets/collision/bullet.tres")

var bullets: Dictionary[RID, Bullet] = {}


func _init_bullet(origin: Vector2, orientation: float, target: Node2D):
	var bullet := Bullet.new()
	# RenderingServer.canvas_item_set_parent(self.ci_rid, get_canvas_item())
	# self.area_rid = PhysicsServer2D.area_create()
	# PhysicsServer2D.area_set_space(self.area_rid, get_world_2d().get_space())
	bullet.init(origin, orientation, target, get_canvas_item(), get_world_2d().get_space())
	bullets[bullet.id] = bullet


func _on_create_bullet(origin: Vector2, orientation: float, target: Node2D):
	_init_bullet(origin, orientation, target)


func _destroy_bullet(bullet: Bullet):
	bullet.destroy()


func _physics_process(delta: float) -> void:
	for bullet: Bullet in bullets.values():
		if bullet.pending_removal:
			continue
		bullet.physics_process(delta)
		if !bullet.pending_removal:
			bullet.update_position()

	var removal: Array[RID] = []
	for bullet: Bullet in bullets.values():
		if bullet.pending_removal:
			removal.push_back(bullet.id)

	for rid in removal:
		_destroy_bullet(bullets[rid])
		bullets.erase(rid)


func _process(_delta: float) -> void:
	# Order the CanvasItem to update every frame.
	queue_redraw()


func _ready():
	SignalBus.create_bullet.connect(_on_create_bullet)


func _exit_tree() -> void:
	for bullet: Bullet in bullets.values():
		_destroy_bullet(bullet)
	bullets.clear()
