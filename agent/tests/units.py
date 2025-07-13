import time
import api_importer as api

def test_spawn(agent, type):
    print(f"Spawnning {type.name}...")
    for i in range(3):
        print(f"{i} -- {agent.spawn_unit(type)}")
        time.sleep(0.5)

agent = api.GameClient(7749, "TOKEN")

test_spawn(agent, api.EnemyType.BUZZY_BEETLE)
test_spawn(agent, api.EnemyType.GOOMBA)
test_spawn(agent, api.EnemyType.KOOPA_JR)
test_spawn(agent, api.EnemyType.KOOPA_PARATROOPA)
test_spawn(agent, api.EnemyType.KOOPA)
test_spawn(agent, api.EnemyType.SPINY_SHELL)
test_spawn(agent, api.EnemyType.WIGGLER)

time.sleep(1)

enemies = agent.get_all_enemies()
if isinstance(enemies, api.ApiException):
    print(f"Error: {repr(enemies)}")
else:
    print(f"{len(enemies)} enemies")
    for i in enemies:
        print(repr(i))
