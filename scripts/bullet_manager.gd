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
	var area_rid: RID
	var ci_rid: RID


# RenderingServer expects references to be kept around
var bullet_texture = preload(
	"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile297.png"
)
var shape = preload("res://assets/collision/bullet.tres")

var bullets: Dictionary[RID, Bullet] = {}


func _init_bullet(origin: Vector2, orientation: float, target: Node2D):
	var bullet := Bullet.new()
	bullet.target = target
	bullet.origin = origin
	bullet.position = origin
	bullet.orientation = orientation
	bullet.area_rid = PhysicsServer2D.area_create()
	bullet.ci_rid = RenderingServer.canvas_item_create()
	PhysicsServer2D.area_set_space(bullet.area_rid, get_world_2d().get_space())
	PhysicsServer2D.area_add_shape(bullet.area_rid, shape)
	# Don't make bullets collidable to improve performance.
	PhysicsServer2D.area_set_collision_layer(bullet.area_rid, 0)
	var callback = func(
		status: int, _area_rid: RID, instance_id: int, _body_shape_idx: int, _self_shape_idx: int
	):
		_on_bullet_body_entered(bullet.area_rid, status, instance_id)
	PhysicsServer2D.area_set_monitor_callback(bullet.area_rid, callback)
	RenderingServer.canvas_item_add_texture_rect(
		bullet.ci_rid,
		Rect2(-bullet_texture.get_size() / 2, bullet_texture.get_size()),
		bullet_texture
	)
	bullets[bullet.area_rid] = bullet


func _on_create_bullet(origin: Vector2, orientation: float, target: Node2D):
	_init_bullet(origin, orientation, target)


func _destroy_bullet(bullet: Bullet):
	PhysicsServer2D.free_rid(bullet.area_rid)
	RenderingServer.free_rid(bullet.ci_rid)


func _on_bullet_body_entered(bullet_area_rid: RID, status: int, instance_id: int):
	if status != PhysicsServer2D.AREA_BODY_ADDED:
		return
	var object = instance_from_id(instance_id)
	if not (object is Node2D and object.is_in_group("EnemyGroup")):
		return
	object.take_damage(damage)
	_destroy_bullet(bullets[bullet_area_rid])
	bullets.erase(bullet_area_rid)


func _physics_process(delta: float) -> void:
	var transform2d := Transform2D()
	var removal: Array[RID] = []
	for bullet: Bullet in bullets.values():
		if !is_instance_valid(bullet.target):
			removal.push_back(bullet.area_rid)
			continue

		var direction = (bullet.target.global_position - bullet.position).normalized()
		var desired_angle = direction.angle()
		bullet.orientation = lerp_angle(bullet.orientation, desired_angle, rotation_speed * delta)
		bullet.position += Vector2.RIGHT.rotated(bullet.orientation) * speed * delta

		var traverse_distance = bullet.position.distance_to(bullet.origin)

		if traverse_distance >= max_distance:
			removal.push_back(bullet.area_rid)
			continue

		transform2d.origin = bullet.position
		var xform = Transform2D().rotated(bullet.orientation).translated(bullet.position)
		PhysicsServer2D.area_set_transform(bullet.area_rid, xform)
		RenderingServer.canvas_item_set_transform(bullet.ci_rid, xform)
		RenderingServer.canvas_item_set_z_index(
			bullet.ci_rid, 20 if traverse_distance >= 10.0 else 0
		)

	for rid in removal:
		_destroy_bullet(bullets[rid])
		bullets.erase(rid)


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
		_destroy_bullet(bullet)
	bullets.clear()
