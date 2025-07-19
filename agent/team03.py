import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

agent = GameClient(7749,"0028f21c")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

# 1. 地形 & set mario
terrain = agent.get_all_terrain()
current_wave = agent.get_current_wave()

if current_wave > -1:
    for a in range(100000000000000000000000000000000000000000000000000000000000000000000000000000000000):

        agent.cast_spell(SpellType.DOUBLE_INCOME)

        for x in range(1,16):
                for y in range(0,19):
                    if(terrain==2):
                        agent.cast_spell(SpellType.TELEPORT,())
                        agent.cast_spell(SpellType.POISON,())
                    else:
                        continue

        agent.spawn_unit(EnemyType.KOOPA_JR)
        agent.spawn_unit(EnemyType.KOOPA)
        agent.spawn_unit(EnemyType.WIGGLER)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        agent.spawn_unit(EnemyType.BUZZY_BEETLE)
        agent.spawn_unit(EnemyType.GOOMBA)

        if agent.get_money(True) > 6100:
            for x in range(1,13):
                for y in range(1,19):
                    if(((terrain[x][y]==1) and (terrain[x][y+1]==2) or (terrain[x+1][y]==2) or (terrain[x][y-1]==2) or (terrain[x-1][y]==2))):
                        pos = Vector2(x,y)
                        agent.place_tower(TowerType.FIRE_MARIO, "3a", pos)
                    else:
                        continue