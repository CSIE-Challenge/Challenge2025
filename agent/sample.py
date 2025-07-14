import time
from api import *

api = GameClient(7749, "cd45de1c") # Replace with your own port and token

# 1: Empty; 2: Road; 3: Obstacle;
def print_all_terrain():
    print("All terrain:")
    Map = api.get_all_terrain()
    for row in Map:
        print("|", end="")
        for terrain in row:
            print(f"{terrain.value}", end="|")
        print()
        for terrain in row:
            print("_"*2, end="")
        print()

print("Running...")

api.send_chat("#It's MARIO time!")

# Get information about terrain
print_all_terrain()
print(api.get_terrain(Vector2(4, 4)))

#Get information about towers, and place a tower if it doesn't exist
if api.get_tower(True, Vector2(8, 5)) is not None:
    print("Tower at (8, 5)")
else:
    print(api.place_tower(TowerType.ICE_LUIGI, "1", Vector2(8, 5)))
print(f"Tower at (8, 5): {api.get_tower(True, Vector2(8, 5))}")

# Spawn Enemy
print(api.spawn_unit(EnemyType.KOOPA))
for i in range(10):
    api.spawn_unit(EnemyType.SPINY_SHELL)
#print(api.get_all_enemies())

#Get information about game state
print(f"Score:{api.get_scores(True)}, Money:{api.get_money(True)}, Income:{api.get_income(True)}")