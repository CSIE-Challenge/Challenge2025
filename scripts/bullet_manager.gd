extends Node2D

@export var speed := 400.0
@export var rotation_speed := 3.0
@export var max_distance := 800.0
@export var damage := 3


class Bullet:
	var target: Node2D = null
	var origin: Vector2
	var position := Vector2()
	var orientation := 0.0
	var body_rid: RID


# RenderingServer expects references to be kept around
var bullet_texture = preload(
	"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile297.png"
)
var shape = preload("res://assets/collision/bullet.tres")

# Dictionary[RID, Bullet]
var bullets: Dictionary = {}


func _init_bullet(origin: Vector2, orientation: float, target: Node2D):
	var bullet := Bullet.new()
	bullet.target = target
	bullet.origin = origin
	bullet.position = origin
	bullet.orientation = orientation
	bullet.body_rid = PhysicsServer2D.body_create()
	PhysicsServer2D.body_set_space(bullet.body_rid, get_world_2d().get_space())
	PhysicsServer2D.body_add_shape(bullet.body_rid, shape)
	# Don't make bullets check collision with other bullets to improve performance.
	PhysicsServer2D.body_set_collision_mask(bullet.body_rid, 0)
	bullets[bullet.body_rid] = bullet


func _on_create_bullet(origin: Vector2, orientation: float, target: Node2D):
	_init_bullet(origin, orientation, target)


func _physics_process(_delta: float) -> void:
	var transform2d := Transform2D()
	for bullet: Bullet in bullets.values():
		transform2d.origin = bullet.position
		PhysicsServer2D.body_set_state(
			bullet.body_rid,
			PhysicsServer2D.BODY_STATE_TRANSFORM,
			Transform2D().rotated(deg_to_rad(bullet.orientation)).translated(bullet.position)
		)


func _process(_delta: float) -> void:
	# Order the CanvasItem to update every frame.
	queue_redraw()


func _draw() -> void:
	var offset := -bullet_texture.get_size() * 0.5
	for bullet: Bullet in bullets.values():
		draw_set_transform(bullet.position, bullet.orientation - PI / 2, Vector2.ONE)
		draw_texture(bullet_texture, offset)


func _ready():
	SignalBus.create_bullet.connect(_on_create_bullet)


func _exit_tree() -> void:
	for bullet: Bullet in bullets.values():
		PhysicsServer2D.free_rid(bullet.body_rid)
	bullets.clear()
