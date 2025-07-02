class_name Bullet

const SPEED := 400.0
const ROATAION_SPEED := 3.0
const MAX_DISTANCE := 800.0
const DAMAGE := 3

const BULLET_TEXTURE = preload(
	"res://assets/kenney_tower-defense-top-down/PNG/Default size/towerDefense_tile297.png"
)
const BULLET_SHAPE = preload("res://assets/collision/bullet.tres")

var area_rid: RID
var ci_rid: RID
var id: RID
var pending_removal: bool = false

var target: Node2D = null
var origin: Vector2
var position := Vector2()
var orientation := 0.0


# `collision_callback` handles collision.
# The arguments is specified by `PhysicsServer2D.area_set_monitor_callback`.
# This function will not be called by bullets pending their removal.
func collision_callback(
	status: int, _area_rid: RID, instance_id: int, _body_shape_idx: int, _self_shape_idx: int
):
	if status != PhysicsServer2D.AREA_BODY_ADDED:
		return
	if !is_instance_id_valid(instance_id):
		return
	var object = instance_from_id(instance_id)
	if not (object is Node2D and object.is_in_group("EnemyGroup")):
		return
	object.take_damage(DAMAGE)
	self.pending_removal = true


# `init` allocates and initalized all properties except for collision shape and canvas texture.
func init(p_origin: Vector2, p_orientation: float, p_target: Node2D, canvas: RID, space: RID):
	self.target = p_target
	self.origin = p_origin
	self.position = self.origin
	self.orientation = p_orientation
	self.register_physics_object(space)
	self.register_canvas_object(canvas)
	self.assign_rid()


# Method `register_physics_object` registers physics resources of the bullet.
# You may want to override this method for finer control over the physics.
# Note that `assign_rid` depends on the `area_rid` to uniquely identify the object.
# If you changed the RID structure, please also modify `assign_rid`.
func register_physics_object(space):
	self.area_rid = PhysicsServer2D.area_create()
	PhysicsServer2D.area_set_space(self.area_rid, space)
	# Don't make bullets collidable to improve performance
	PhysicsServer2D.area_set_collision_layer(self.area_rid, 0)

	var callback = func(status, area_rid, instance_id, body_shape_idx, self_shape_idx):
		if !self.pending_removal:
			self.collision_callback(status, area_rid, instance_id, body_shape_idx, self_shape_idx)

	PhysicsServer2D.area_set_monitor_callback(self.area_rid, callback)
	self.register_shape()


# Method `register_shape` registers the collision shape.
# You may want to override this for changing the shape only.
func register_shape():
	PhysicsServer2D.area_add_shape(self.area_rid, BULLET_SHAPE)


# Method `register_canvas_object` registers texture of this bullet.
# You may want to override this for finer control over the textures.
func register_canvas_object(canvas):
	self.ci_rid = RenderingServer.canvas_item_create()
	RenderingServer.canvas_item_set_parent(self.ci_rid, canvas)
	self.register_texture()


# Method `register_texture` registers the bullet texture.
# You may want to override this for changing the textures only.
func register_texture():
	RenderingServer.canvas_item_add_texture_rect(
		self.ci_rid,
		Rect2(-BULLET_TEXTURE.get_size() / 2, BULLET_TEXTURE.get_size()),
		BULLET_TEXTURE
	)


# `assign_rid` takes an RID as this object's tracking RID.
# The `id` will be `area_rid` by default.
# If physics of the bullet is changed, please override this method.
func assign_rid():
	self.id = area_rid


# Method `physics_process` controls the behavior of the bullet.
func physics_process(delta):
	if !is_instance_valid(self.target):
		self.pending_removal = true
		return

	var direction = (self.target.global_position - self.position).normalized()
	var desired_angle = direction.angle()
	self.orientation = lerp_angle(self.orientation, desired_angle, ROATAION_SPEED * delta)
	self.position += Vector2.RIGHT.rotated(self.orientation) * SPEED * delta

	var traverse_distance = self.position.distance_to(self.origin)

	if traverse_distance >= MAX_DISTANCE:
		self.pending_removal = true
		return


# Method `update_physics` controls both the physics and the texture position.
func update_position():
	var xform = Transform2D().rotated(self.orientation - PI / 2).translated(self.position)
	PhysicsServer2D.area_set_transform(self.area_rid, xform)
	RenderingServer.canvas_item_set_transform(self.ci_rid, xform)
	var traverse_distance = self.position.distance_to(self.origin)
	RenderingServer.canvas_item_set_z_index(self.ci_rid, 20 if traverse_distance >= 10.0 else 0)


# Method `destroy` deallocates all resources of the bullet.
func destroy():
	PhysicsServer2D.area_set_monitor_callback(self.area_rid, Callable())
	PhysicsServer2D.free_rid(self.area_rid)
	RenderingServer.canvas_item_clear(self.ci_rid)
