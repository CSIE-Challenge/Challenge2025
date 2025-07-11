import time
from api import *

api = GameClient(7749, "76a2efd2")

print(api.get_scores(True))
print(api.get_scores(False))

terrain = api.get_all_terrain()
for i in range(4):
    for j in range(4):
        print(f"{repr(terrain[i][j]):27s}", end="")
    print()

ret = api.get_all_towers(True)
if not ret:
    print("no tower found")
    
print(api.get_tower(Vector2(8, 4)))
print(api.place_tower(TowerType.ICE_LUIGI, Vector2(8, 4)))
print(api.get_tower(Vector2(8, 4)))

for i in range(5):
    api.spawn_unit(EnemyType.SPINY_SHELL)
    time.sleep(3)