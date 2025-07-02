class_name SignalBus
extends Node2D

# This signal passes a bullet with parameters set (`set_params`) called,
# but not yet allocated all related objects. This is because the context
# of the bullet creator might be different from the BulletManager, so it
# must be initialized and allocated later instead. For example of usage,
# please refer to the default Tower.
signal create_bullet(bullet: Bullet)
