from time import sleep
import api_importer as api
from test_token import TOKEN1

agent = api.GameClient(7749, TOKEN1)


def place_towers(tower_type, x, y):
    lvls = ["1", "2a", "2b", "3a", "3b"]
    for i in range(5):
        print(
            f"placing tower {tower_type.name}: {repr(agent.place_tower(tower_type, lvls[i], api.Vector2(x, y + i)))}"
        )


# set initial money to a large number before running this
# works on map 椰林大道
place_towers(api.TowerType.DONKEY_KONG, 11, 8)
place_towers(api.TowerType.FIRE_MARIO, 12, 8)
place_towers(api.TowerType.FORT, 13, 8)
place_towers(api.TowerType.ICE_LUIGI, 11, 13)
place_towers(api.TowerType.SHY_GUY, 12, 13)

print(agent.place_tower(api.TowerType.DONKEY_KONG, "1", api.Vector2(1, 3)))
print(agent.place_tower(api.TowerType.DONKEY_KONG, "1", api.Vector2(0, 3)))

towers = agent.get_all_towers(True)
if isinstance(towers, api.ApiException):
    print(repr(towers))
else:
    print(f"{len(towers)} towers")
    for tower in towers:
        print(f"{tower.position} Tower {tower.type.name}: {repr(tower)}")
        # print(f"    level_a = {tower.level_a}")
        # print(f"    level_b = {tower.level_b}")
        # print(f"    aim = {tower.aim}")
        # print(f"    anti_air = {tower.anti_air}")
        # print(f"    reload = {tower.reload}")
        # print(f"    range = {tower.range}")
        # print(f"    damage = {tower.damage}")
        # print(f"    bullet_effect = {tower.bullet_effect}")

print(f"( 11,   9) -- {repr(agent.get_tower(True, api.Vector2(11, 9)))}")
print(f"( 13,  10) -- {repr(agent.get_tower(True, api.Vector2(13, 10)))}")
print(f"( 13,  14) -- {repr(agent.get_tower(True, api.Vector2(13, 14)))}")  # empty
print(
    f"(100, 100) -- {repr(agent.get_tower(True, api.Vector2(100, 100)))}"
)  # out of bound
print(
    f"( -1,  -1) -- {repr(agent.get_tower(True, api.Vector2(-1, -1)))}"
)  # out of bound

sleep(5)

for x in range(11, 14):
    for y in range(8, 18):
        print(f"selling ({x}, {y}): {agent.sell_tower(api.Vector2(x, y))}")
