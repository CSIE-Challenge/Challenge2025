import time
from api import *

api = GameClient(7749, "eaa01c9c")

print(api.get_scores(True))
print(api.get_scores(False))

terrain = api.get_all_terrain()
for i in range(4):
    for j in range(4):
        print(f"{repr(terrain[i][j]):27s}", end="")
    print()


print(api.place_tower(TowerType.ICE_LUIGI, "2a", Vector2(8, 4)))
time.sleep(3)
print(api.place_tower(TowerType.SHY_GUY, "3b", Vector2(8, 4)))
time.sleep(3)
print(api.place_tower(TowerType.SHY_GUY, "3a", Vector2(8, 4)))
time.sleep(3)
print(api.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 4)))
time.sleep(3)
print(api.place_tower(TowerType.FIRE_MARIO, "3c", Vector2(8, 4)))