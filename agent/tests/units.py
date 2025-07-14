import time
import api_importer as api
from test_token import TOKEN1


def test_spawn(agent, type):
    print(f"Spawning {type.name}...")
    print(f"  1st -- {agent.spawn_unit(type)}")
    print(f"  2nd -- {agent.spawn_unit(type)}")
    cd = agent.get_unit_cooldown(type)
    print(f"  cooldown -- {cd}")
    if not isinstance(cd, api.ApiException):
        time.sleep(cd + 0.5)
        print(f"  3nd -- {agent.spawn_unit(type)}")
    time.sleep(0.5)


agent = api.GameClient(7749, TOKEN1)

test_spawn(agent, api.EnemyType.BUZZY_BEETLE)
test_spawn(agent, api.EnemyType.GOOMBA)
test_spawn(agent, api.EnemyType.KOOPA_JR)
test_spawn(agent, api.EnemyType.KOOPA_PARATROOPA)
test_spawn(agent, api.EnemyType.KOOPA)
test_spawn(agent, api.EnemyType.SPINY_SHELL)
test_spawn(agent, api.EnemyType.WIGGLER)

time.sleep(1)

enemies = agent.get_all_enemies(True)
if isinstance(enemies, api.ApiException):
    print(f"Error: {repr(enemies)}")
else:
    print(f"{len(enemies)} enemies")
    for i in enemies:
        print(repr(i))

enemies = agent.get_all_enemies(False)
if isinstance(enemies, api.ApiException):
    print(f"Error: {repr(enemies)}")
else:
    print(f"{len(enemies)} enemies")
    for i in enemies:
        print(repr(i))
