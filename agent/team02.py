# Copyright © 2025 mtmatt, ouo. All rights reserved.

import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

agent = GameClient(7749, "c487fe19")  # Replace with your token

agent.set_the_radiant_core_of_stellar_faith(7785)

def ntu_student_id_card(self):
    """Returns the NTU student ID card number."""
    print(agent.ntu_student_id_card())
    return "123456789"

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")
print("a")
# Chat
agent.set_name("O.o")
agent.set_chat_name_color("#FF0000")
cat = agent.pixelcat()
print(agent.pixelcat())
print(cat)
agent.send_chat(cat)
sent = agent.send_chat("You are gay! <3")


mario_towers = 0
terrain = agent.get_all_terrain()
path = agent.get_system_path(False)  # List[Vector2]

path_set = set((p.x, p.y) for p in path)

rows = len(terrain)
cols = len(terrain[0])

list_mario = []
list_fort = []
for row in range(rows):
        for col in range(cols):
            if terrain[row][col] == TerrainType.EMPTY:
                tmp = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dx, col + dy
                    if (nr, nc) in path_set:
                        list_mario.append(Vector2(row, col))
                        tmp = 1
                        break
                if tmp == 0:
                     list_fort.append(Vector2(row, col))
    


                        
while True:

    remain_time = agent.get_remain_time()
    wave = agent.get_current_wave()
    agent.send_chat('1')
    terrain_ground = agent.get_system_path(False)
    
    terrain = agent.get_all_terrain() # 地形
    path = agent.get_system_path(False)  # List[Vector2]
    enemy = agent.get_all_enemies(True) # 我方資訊

    path_set = set((p.x, p.y) for p in path)

    rows = len(terrain)
    cols = len(terrain[0])

    if remain_time <= 10.0 :
        agent.super_star()

    if remain_time <= 60.0 :
        agent.boo()

    terrain_fly = agent.get_system_path(True)
    for cell in terrain_fly:
            if agent.get_terrain(cell) == TerrainType.EMPTY and agent.get_tower((True), cell) != TowerType.ICE_LUIGI:
                agent.place_tower(TowerType.FIRE_MARIO, '1', cell)
                mario_towers += 1

    if agent.get_money(True) >= 5000:
        agent.spawn_unit(EnemyType.KOOPA)
    # CAST DOUBLE INCOME
    agent.cast_spell(SpellType.DOUBLE_INCOME)

    # teleport
    for e in enemy:
        if e.position.x == path[1].x and e.position.y == path[1].y:
            if wave <= 3: 
                agent.cast_spell(SpellType.TELEPORT, path[2])
                agent.send_chat('3')
            else:
                agent.cast_spell(SpellType.TELEPORT, path[3])
                agent.send_chat('3')
    

    if remain_time <= 292:   
        agent.cast_spell(SpellType.POISON, path[2])
        if agent.get_spell_cooldown(True,SpellType.POISON) == 0:
            agent.cast_spell(SpellType.POISON, path[5])
    # ATTACK
    if agent.get_money(True) >= 3000:
        agent.spawn_unit(EnemyType.KOOPA_JR)
    agent.send_chat('5')   
                 
    terrain = agent.get_all_terrain()
    path = agent.get_system_path(False)  # List[Vector2]

    path_set = set((p.x, p.y) for p in path)

    rows = len(terrain)
    cols = len(terrain[0])

    for row in range(rows):
        for col in range(cols):
            if terrain[row][col] == TerrainType.EMPTY:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = row + dx, col + dy
                    if (nr, nc) in path_set:
                        if remain_time >= 90:
                            if mario_towers % 2 ==0:
                                if agent.get_tower((True), Vector2(row, col)) != TowerType.FIRE_MARIO and remain_time < 270:
                                    agent.place_tower(TowerType.ICE_LUIGI, '1', Vector2(row, col))
                                    if agent.get_tower((True), Vector2(row, col)) == TowerType.FIRE_MARIO:
                                        mario_towers += 1
                            else:
                                if agent.get_tower((True), Vector2(row, col)) != TowerType.ICE_LUIGI:
                                    agent.place_tower(TowerType.FIRE_MARIO, '1', Vector2(row, col))
                                    mario_towers += 1
                        else:
                            agent.place_tower(TowerType.FORT, '2b', Vector2(row, col))
                        break
    
    if remain_time < 150:
        for row in range(rows):
            for col in range(cols):
                if terrain[row][col] == TerrainType.EMPTY:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dx, col + dy
                        if (nr, nc) in path_set:
                            if mario_towers % 2 ==0:
                                if agent.get_tower((True), Vector2(row, col)) != TowerType.FIRE_MARIO:
                                    agent.place_tower(TowerType.ICE_LUIGI, '2b', Vector2(row, col))
                                    mario_towers+=1
                                    agent.send_chat("s")
                            else:
                                if agent.get_tower((True), Vector2(row, col)) != TowerType.ICE_LUIGI:
                                    agent.place_tower(TowerType.FIRE_MARIO, '2a', Vector2(row, col))
                                    mario_towers+=1
                                    agent.send_chat("y")
                            break
    
    if remain_time <= 60:
        for row in range(rows):
            for col in range(cols):
                agent.sell_tower(Vector2(row, col))
        while True:
            agent.spawn_unit(EnemyType.KOOPA_JR)
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            agent.spawn_unit(EnemyType.GOOMBA)
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
            agent.spawn_unit(EnemyType.WIGGLER)
            agent.spawn_unit(EnemyType.KOOPA)
            agent.spawn_unit(EnemyType.SPINY_SHELL)
