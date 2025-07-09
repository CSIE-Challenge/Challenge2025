import time
from api import *

api = GameClient(7749, "TOKEN")

print(api.get_scores(True))
print(api.get_scores(False))

terrain = api.get_all_terrain()
for i in range(4):
    for j in range(4):
        print(f"{repr(terrain[i][j]):27s}", end="")
    print()

print(api.place_tower(TowerType.BASIC, Vector2(2, 2)))
print(api.get_all_towers(True))
