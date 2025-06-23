extends RigidBody2D

@onready var turret = $Turret
@onready var enemy_detector = $AimRange/CollisionShape2D

var built: bool = false
var damage: int = 0
var rotation_speed: float = 90.0 # degree per second
var aim_range: float = 450.0
var level: int = 1
var current_shoot_turret: int = 0 # 0 for left, 1 for right

var enemies: Array = []

func _ready() -> void:
    enemy_detector.shape.radius = 0.5 * aim_range

func _process(delta: float) -> void:
    pass

func _physics_process(delta: float) -> void:
    #print(enemies)
    if enemies.size() > 0:
        aim(delta)

func aim(delta: float) -> void:
    var first_enemy = enemies[0]
    var pos_diff: Vector2 = self.position - first_enemy.position
    var angle: float = atan2(pos_diff.y, pos_diff.x)
    var angle_diff = angle - turret.rotation - PI/2
    if angle_diff < -2 * PI:
        angle_diff += 2 * PI
    print(angle_diff)
    if (angle_diff < PI and angle_diff > 0) or (angle_diff < -PI and angle_diff > -2 * PI):
        turret.rotate(delta * deg_to_rad(rotation_speed))
    else:
        turret.rotate(-delta * deg_to_rad(rotation_speed))

func shoot() -> void:
    pass


func _on_aim_range_body_entered(body: Node2D) -> void:
    if body == self:
        return
    enemies.append(body.get_parent())


func _on_aim_range_body_exited(body: Node2D) -> void:
    enemies.erase(body.get_parent())
