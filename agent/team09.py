# Copyright © 2025 mtmatt, ouo. All rights reserved.

import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource
import random
agent = GameClient(7749, "7aee129e")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

newmoney = agent.get_the_radiant_core_of_stellar_faith()
if newmoney >= 4500:
    agent.ntu_student_id_card()

# 1. 地形
"""
coco = [[]]
terrain = agent.get_all_terrain()
for row in terrain:
    for t in row:
        t.value
    print()
print("Single terrain at (4,4):", agent.get_terrain(Vector2(4, 4)), "\n")

# 2. 分數、金錢、收入
print("Scores:", agent.get_scores(True), "(Me) /", agent.get_scores(False), "(Opp)")
print("Money: ", agent.get_money(True), "(Me) /", agent.get_money(False), "(Opp)")
print("Income:", agent.get_income(True), "(Me) /", agent.get_income(False), "(Opp)\n")

# 3. 波次與時間
print("Wave:", agent.get_current_wave())
print("Remain time:", f"{agent.get_remain_time():.2f}s")
print("Until next wave:", f"{agent.get_time_until_next_wave():.2f}s\n")

# 4. 路徑
print("System path (ground):", [(c.x, c.y) for c in agent.get_system_path(False)])
print("Opponent path (air):",  [(c.x, c.y) for c in agent.get_opponent_path(True)], "\n")

# 5. 塔操作
pos = Vector2(5, 5)
if agent.get_tower(True, pos) is None:
    print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
    #agent.place_tower(TowerType.FIRE_MARIO, "1", pos)
print("All my towers:", agent.get_all_towers(True))
# 設定塔的攻擊模式
agent.set_strategy(pos, TargetStrategy.CLOSE)

if agent.get_tower(True, Vector2(1, 2)) is None:
    agent.place_tower(TowerType.ICE_LUIGI, "1", pos)
#time.sleep(3)
# 賣塔
agent.sell_tower(Vector2(1, 1))
print("After sell:", agent.get_all_towers(True), "\n")

# 6. 出兵
agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
print("Opp enemies:", agent.get_all_enemies(False))
print("KOOPA cooldown:", f"{agent.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA):.2f}s\n")

# 7. 法術
#agent.cast_spell(SpellType.POISON, Vector2(3, 3))
print("My POISON CD:", f"{agent.get_spell_cooldown(True, SpellType.POISON):.2f}s\n")

# 8. 聊天
agent.set_name("OuO")
agent.set_chat_name_color("DCB5FF")
sent = agent.send_chat("OuO love you ! <3")
history = agent.get_chat_history(5)
for src, msg in history:
    if src == ChatSource.PLAYER_SELF:
        who = "OuO"
    elif src == ChatSource.PLAYER_OTHER:
        who = "Loser"
    else:
        who = "System"
    print(f"[{who}]", msg)
print()
"""
########## judge map
terrain=agent.get_all_terrain()
terrain_one = agent.get_terrain(Vector2(1, 3))
terrain_two = agent.get_terrain(Vector2(2, 3))
print(terrain_one,terrain_two)
def map_type():

    def mapmatch(map1,map2):
        for i in range(len(terrain)):
            for j in range(len(terrain[0])):
                if map1[i][j] != map2[i][j]:
                    return False
        return True
    
    map1 = [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,1,1,3,3,3,3,3,3,2,3,1,3,3,3,3,3,3,3,3,3],[3,1,1,3,3,3,1,1,1,2,3,1,3,3,3,3,3,3,3,3,3],[3,2,2,2,2,2,2,2,2,2,3,3,1,2,2,2,2,2,3,3,3],[3,1,3,3,3,3,1,3,1,2,3,3,3,2,1,1,1,2,3,3,3],[3,1,3,3,3,3,1,3,3,2,3,3,3,2,1,1,1,2,3,3,3],[3,1,1,1,1,1,1,3,3,2,1,3,3,2,1,3,1,2,1,3,3],[3,1,1,2,2,2,2,2,2,2,3,3,1,2,1,3,1,2,1,1,3],[3,1,1,2,1,1,1,1,3,3,3,3,1,2,3,3,1,2,1,1,3],[3,1,1,2,1,1,1,1,3,3,3,3,1,2,3,3,1,2,1,1,3],[3,1,1,2,1,1,1,1,3,3,3,3,1,2,1,1,1,2,1,1,3],[3,1,1,2,1,1,1,1,3,3,1,3,1,2,1,1,1,2,1,1,3],[3,1,1,2,2,2,2,2,2,2,2,2,2,2,3,3,3,2,3,1,3],[3,3,3,3,3,3,1,1,1,1,1,1,1,1,3,3,3,3,3,1,3],[3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,1,1,3,3,1,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]
    map2 = [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,1,1,1,1,3,1,1,1,1,1,1,3,1,1,1,1,1,1,1,3],[3,1,1,2,1,1,1,2,1,1,2,2,2,3,1,1,3,1,1,1,3],[3,1,1,2,1,3,1,2,3,1,2,1,3,2,3,1,1,1,1,1,3],[3,1,1,2,1,1,1,2,1,1,2,1,1,3,2,3,1,1,3,1,3],[3,1,1,2,1,1,1,2,1,1,2,3,1,1,3,2,3,1,1,1,3],[3,1,2,2,1,1,2,2,1,1,2,2,2,1,1,3,2,3,1,1,3],[3,1,2,1,1,1,2,3,3,3,1,1,2,1,1,1,3,2,1,1,3],[3,1,2,1,3,1,2,3,3,3,3,1,2,1,1,1,1,2,1,1,3],[3,1,2,1,1,1,2,2,3,3,1,1,2,1,3,1,1,2,1,3,3],[3,3,2,2,1,1,1,2,1,1,2,2,2,1,1,1,1,2,1,1,3],[3,1,1,2,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1,1,3],[3,3,1,2,2,2,2,2,2,2,2,1,1,1,1,3,3,2,1,1,3],[3,1,1,1,1,1,1,1,1,1,1,1,3,3,3,1,1,1,3,3,3],[3,1,1,1,3,1,1,1,3,3,1,1,3,3,3,1,1,1,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]
    map3 = [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,3],[3,3,3,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,3],[3,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,3],[3,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,3],[3,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,3],[3,3,1,2,1,3,3,3,1,3,3,1,1,1,1,1,2,1,1,1,3],[3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,3],[3,3,1,1,1,1,3,3,3,1,3,1,1,1,1,1,2,1,1,1,3],[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,3],[3,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,3],[3,1,1,3,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,3,3],[3,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,3,3,3],[3,1,1,3,1,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,3],[3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]
    map4 = [[3,3,3,3,2,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3],[2,2,2,3,2,3,1,1,1,3,1,1,1,3,2,3,3,3,3,3,3],[3,3,2,2,2,3,1,1,1,3,1,1,1,2,2,3,2,2,2,2,2],[3,1,1,3,2,2,3,3,3,3,3,3,3,2,3,2,2,3,3,3,3],[3,1,1,2,2,2,3,3,3,3,3,3,3,2,3,2,3,3,3,3,3],[3,3,1,2,3,2,1,1,1,3,1,1,1,2,2,2,2,2,1,1,3],[3,3,2,2,3,2,1,1,1,3,1,1,1,1,2,1,1,2,2,1,3],[3,3,2,1,1,2,3,3,3,3,3,1,1,1,2,1,1,1,2,2,3],[3,3,2,1,3,2,3,3,3,2,2,2,2,1,2,1,1,1,1,2,3],[3,3,2,1,1,2,3,3,2,2,1,1,2,2,2,2,3,3,2,2,3],[3,3,2,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,3,3],[3,2,2,2,3,3,3,2,2,2,1,1,1,3,2,2,1,1,1,1,3],[3,2,3,2,2,2,2,2,2,2,2,2,1,2,2,1,1,1,1,1,3],[3,2,2,3,2,2,3,3,1,1,1,2,2,2,1,1,1,1,1,1,3],[3,3,2,2,2,3,3,3,1,1,1,1,3,3,1,1,1,1,1,1,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]
    map5 = [[3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,2,3,3,3,1,1,3,3,1,1,1,1,1,3,3,1,3,3,3],[3,3,2,1,1,1,1,2,2,2,2,2,2,1,3,1,1,2,3,3,3],[3,3,2,1,1,1,1,2,1,1,1,1,2,3,1,1,1,2,3,3,3],[3,3,2,1,1,1,3,2,1,1,1,1,2,3,1,1,1,2,3,3,3],[3,3,2,1,3,3,3,2,1,1,1,1,2,3,1,1,3,2,3,3,3],[3,3,2,3,3,3,3,2,2,2,2,2,2,1,1,1,3,2,3,3,3],[3,3,2,3,3,3,3,2,3,1,3,3,2,1,3,3,3,2,1,3,3],[3,3,2,3,3,1,3,2,1,1,1,3,2,1,3,3,3,2,1,3,3],[3,3,2,2,2,2,2,2,1,1,1,3,2,1,3,3,3,2,1,3,3],[3,3,2,3,3,1,1,2,1,1,1,3,2,2,2,2,2,2,1,3,3],[3,3,2,3,3,1,1,2,1,1,1,3,2,3,3,1,1,2,3,3,3],[3,3,2,3,3,1,1,2,1,1,1,3,2,3,3,1,1,2,1,1,3],[3,1,2,2,2,2,2,2,1,1,1,3,2,3,3,1,1,2,1,1,3],[3,1,1,3,3,3,3,3,1,1,1,3,2,2,2,2,2,2,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]

    terrain = [[0 for j in range(21)] for i in range(16)]
    terrain_tmp=agent.get_all_terrain()
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            terrain[i][j] = terrain_tmp[i][j]
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            print(str(map1[i][j])+' ',end='')
        print()
    print()
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            print(str(terrain[i][j])+' ',end='')
        print()
    print()
    
    if mapmatch(terrain,map1):
        return 'gen'
    if mapmatch(terrain,map2):
        return 'town'
    if mapmatch(terrain,map3):
        return 'coco'
    if mapmatch(terrain,map4):
        return 'space'
    if mapmatch(terrain,map5):
        return 'gen'
    return 'gen'


wave = 0
map_name = map_type()
terrain = agent.get_all_terrain()
for row in terrain:
    for t in row:
        print(f"{t.value:2d}", end=" ")
    print()
print(map_name)

###### coco map ##########################################################
loop_counter = 0
coco_init = 0
gen_init = 0
remain_time = 300.0
center_cnt = 0
usedcnt = 0
ni = 0
terrain = agent.get_all_terrain()
terrain_t = list(zip(*terrain))
h = len(terrain_t)
w = len(terrain_t[0]) if h > 0 else 0
print(f'h = {h}, w = {w}')
cornerlist_i = []
cornerlist_j = []
cornerlist = []
cornerused = []
for i in range(h):
    for j in range(w):
        center_cnt = 0
        center = terrain_t[i][j]
        if center != 1: 
            continue
        if terrain_t[i-1][j] == 2: center_cnt += 1
        if terrain_t[i+1][j] == 2: center_cnt += 1
        if terrain_t[i][j-1] == 2: center_cnt += 1
        if terrain_t[i][j+1] == 2: center_cnt += 1
        if center_cnt >= 2:
            print("轉角: ",i,",",j)
            #agent.place_tower(TowerType.FORT, "1", Vector2(j, i))
            cornerlist.append(Vector2(j, i))
            print(f'append: {cornerlist[len(cornerlist) - 1].x}, {cornerlist[len(cornerlist) - 1].y}')
            cornerused.append(0)
            cornerlist_i.append(j)
            cornerlist_j.append(i)
while True:
    loop_counter += 1
    #get income
    income = agent.get_income(True)
    # for coco, put three pipes
    if coco_init == 0 and map_name == 'coco':
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 2))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 17))
        temp1 = agent.get_tower(True, Vector2(4, 2))
        temp2 = agent.get_tower(True, Vector2(7, 17))
        temp3 = agent.get_tower(True, Vector2(10, 17))
        if temp1 != None and temp2 != None and temp3 != None:##########start here
            coco_init += 1
            #print('tower is success')

    # for coco, after three pipes
    if coco_init == 1 and map_name == 'coco':
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 1))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(11, 7))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9, 8))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(3, 12))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(5, 12))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 19))
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 15))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 18))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 19))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 3))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 4))
        
        #check
        temp1 = agent.get_tower(True, Vector2(10, 17))
        temp2 = agent.get_tower(True, Vector2(10, 18))
        temp3 = agent.get_tower(True, Vector2(10, 19))
        temp4 = agent.get_tower(True, Vector2(7, 18))
        temp5 = agent.get_tower(True, Vector2(7, 19))
        temp6 = agent.get_tower(True, Vector2(4, 1))
        temp7 = agent.get_tower(True, Vector2(3, 12))
        temp8 = agent.get_tower(True, Vector2(5, 12))
        temp9 = agent.get_tower(True, Vector2(10, 3))
        temp10 = agent.get_tower(True, Vector2(10, 4))
        temp11 = agent.get_tower(True, Vector2(4, 15))
        temp12 = agent.get_tower(True, Vector2(11, 7))
        temp13 = agent.get_tower(True, Vector2(9, 8))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None and temp9 != None and temp10 != None and temp11 != None and temp12 != None and temp13 != None:
            coco_init += 1

    #for coco, Mairo
    if coco_init == 2 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(3, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(5, 14))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(6, 12))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(4, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 8))
        #check
        temp1 = agent.get_tower(True, Vector2(3, 13))
        temp2 = agent.get_tower(True, Vector2(5, 14))
        temp3 = agent.get_tower(True, Vector2(6, 12))
        temp4 = agent.get_tower(True, Vector2(9, 10))
        temp5 = agent.get_tower(True, Vector2(4, 15))
        temp6 = agent.get_tower(True, Vector2(11, 8))
        
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            coco_init += 1

    #for coco, remining da sing sing
    if coco_init == 3 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(5, 4))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(6, 4))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(8, 15))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(9, 15))
        temp1 = agent.get_tower(True, Vector2(5, 4))
        temp2 = agent.get_tower(True, Vector2(6, 4))
        temp3 = agent.get_tower(True, Vector2(8, 15))
        temp4 = agent.get_tower(True, Vector2(9, 15))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None:
            coco_init += 1

    #for coco, ice
    if coco_init == 4 and map_name == 'coco':
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(3, 12))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 5))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(8, 9))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 9))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(6, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(8, 14))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(9, 14))
        #check
        temp1 = agent.get_tower(True, Vector2(3, 12))
        temp2 = agent.get_tower(True, Vector2(5, 5))
        temp3 = agent.get_tower(True, Vector2(8, 9))
        temp4 = agent.get_tower(True, Vector2(5, 9))
        temp5 = agent.get_tower(True, Vector2(6, 11))
        temp6 = agent.get_tower(True, Vector2(8, 14))
        temp7 = agent.get_tower(True, Vector2(9, 14))
        temp8 = agent.get_tower(True, Vector2(5, 11))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None:
            coco_init += 1

    

    #for coco, da sing sing & Mario ver.2
    if coco_init == 5 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3b", Vector2(11, 6))
        agent.place_tower(TowerType.DONKEY_KONG, "3b", Vector2(12, 6))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(8, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 8))
        temp1 = agent.get_tower(True, Vector2(11, 6))
        temp2 = agent.get_tower(True, Vector2(12, 6))
        temp3 = agent.get_tower(True, Vector2(8, 13))
        temp4 = agent.get_tower(True, Vector2(9, 13))
        temp5 = agent.get_tower(True, Vector2(11, 10))
        temp6 = agent.get_tower(True, Vector2(11, 11))
        temp7 = agent.get_tower(True, Vector2(9, 8))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None:
            coco_init += 1

    #for coco, last luan fang
    if coco_init == 6 and map_name == 'coco':
        x = 9
        for y in range(5, 16):
            temp1 = agent.get_tower(True, Vector2(x, y))
            if temp1 == None:
                if y % 3 == 0:
                    agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(x, y))
                elif y % 3 == 1:
                    agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(x, y))
                else:
                    agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(x, y))

        x = 11
        for y in range(6, 17):
            temp1 = agent.get_tower(True, Vector2(x, y))
            if temp1 == None:
                if y % 3 == 0:
                    agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(x, y))
                elif y % 3 == 1:
                    agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(x, y))
                else:
                    agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(x, y))
        
    #for coco, double money spell
    if map_name == 'coco' and remain_time <= 270.0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    
    #for coco, teleport
    if map_name == 'coco':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.type == EnemyType.KOOPA:
                print('find koppa')
                #time.sleep(3)
                print('koppa pos: ', end = "")
                print(i.position)
                print(type(i.position))
                ###
                '''if i.position.x == 4 and i.position.y == 19:
                    print("jkxcvh")
                    time.sleep(3)
                if i.position == Vector2(4, 19) or i.position == Vector2(4, 18) or i.position == Vector2(4, 17) or i.position == Vector2(4, 16) or i.position == Vector2(5, 16) or i.position == Vector2(6, 16):
                    print('at correct pos')
                    #time.sleep(3)
                    agent.cast_spell(SpellType.TELEPORT, i.position)'''
                if i.position.x == 4:
                    if i.position.y == 19 or i.position.y == 18 or i.position.y == 17:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x, i.position.y -1))
                elif i.position.y == 16:
                    if i.position.x == 4 or i.position.x == 5 or i.position.x == 6:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x +1, i.position.y))
                

    #for coco, poison
    if map_name == 'coco':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.position.x == 10 and i.position.y == 5:
                agent.cast_spell(SpellType.POISON, Vector2(12, 5))
                break

    #for coco, li_bao_bao
    if loop_counter % 4 == 0 and coco_init >= 1 and coco_init <= 2: ################################
        agent.spawn_unit(EnemyType.GOOMBA)
        print('li bao bao success')

    #for coco, flying turtles
    if coco_init >= 4:
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        print('flying turtle success')

    ###############################################################
    #for general case, long road put pipe
    """
    longroadlist = []
    longroadlist.append(Vector2(0, 0))
    if map_type == 'gen' and gen_init == 0:
        for i in range(1, 15):
            for start in range(1, 10): #10 = 20 - 10
                flag = 0
                for j in range(0, 10):
                    if terrain[i][start + j] != TerrainType.ROAD:
                        flag = 1
                        break
                if flag == 0:
                    longroadlist.append(Vector2(i, j))
        for i in range(1, 20):
            for start in range(1, 5):
                flag = 0
                for j in range(0, 10):
                    if terrain[i][start + j] != TerrainType.ROAD:
                        flag = 1
                        break
                if flag == 0:
                    longroadlist.append(Vector2(i, j))
    print(longroadlist)
    """
    #for general case, da sing sing at corner
    
    if map_name == 'gen' and gen_init == 0:
        for i in range(0, len(cornerlist)):
            temp = agent.get_tower(True, cornerlist[i])
            if temp == None:
                agent.place_tower(TowerType.DONKEY_KONG, "1", cornerlist[i])
                temp = agent.get_tower(True, cornerlist[i])
                if temp != None:
                    usedcnt += 1
                    print(f'used cnt = {usedcnt}')
            if usedcnt == len(cornerlist):
                gen_init = 1
                break
    #for general case, ice at aside
    if map_name == 'gen' and gen_init == 1:
        print('here')
        usedcnt = 0
        
        #for i in range(0, len(cornerlist)):
        nx = cornerlist[ni].x
        ny = cornerlist[ni].y
        if nx - 1 >= 1 and agent.get_terrain(Vector2(nx - 1, ny)) == TerrainType.EMPTY and agent.get_tower(True, Vector2(nx - 1, ny)) == None:
            agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(nx - 1, ny))
            if agent.get_tower(True, Vector2(nx - 1, ny)) != None and agent.get_tower(True, Vector2(nx - 1, ny)) == TowerType.ICE_LUIGI:
                ni += 1
        elif nx + 1 <= 14 and agent.get_terrain(Vector2(nx + 1, ny)) == TerrainType.EMPTY and agent.get_tower(True, Vector2(nx + 1, ny)) == None:
            agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(nx + 1, ny))
            if agent.get_tower(True, Vector2(nx + 1, ny)) != None and agent.get_tower(True, Vector2(nx + 1, ny)).type == TowerType.ICE_LUIGI:
                ni += 1
        elif ny + 1 <= 19 and agent.get_terrain(Vector2(nx, ny + 1)) == TerrainType.EMPTY and agent.get_tower(True, Vector2(nx, ny + 1)) == None:
            agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(nx, ny + 1))
            if agent.get_tower(True, Vector2(nx, ny + 1)) != None and agent.get_tower(True, Vector2(nx, ny + 1)).type == TowerType.ICE_LUIGI:
                ni += 1
        elif ny - 1 >= 1 and agent.get_terrain(Vector2(nx, ny - 1)) == TerrainType.EMPTY and agent.get_tower(True, Vector2(nx, ny - 1)) == None:
            agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(nx, ny - 1))
            if agent.get_tower(True, Vector2(nx, ny - 1)) != None and agent.get_tower(True, Vector2(nx, ny - 1)).type == TowerType.ICE_LUIGI:
                ni += 1
        if agent.get_money(True) >= 1500:
            ni += 1
        if ni == len(cornerlist):
            gen_init += 1
    #for general, upgrade da sing sing
    if map_name == 'gen' and gen_init == 2:
        towerlist = agent.get_all_towers(True)
        for i in towerlist:
            if i.type == TowerType.DONKEY_KONG:
                #agent.sell_tower(i.position)
                agent.place_tower(TowerType.DONKEY_KONG, "3a", i.position)
        if agent.get_money(True) >= 3500:
            gen_init += 1

    #for general, upgrade ice
    if map_name == 'gen' and gen_init == 3:
        towerlist = agent.get_all_towers(True)
        for i in towerlist:
            if i.type == TowerType.ICE_LUIGI:
                #agent.sell_tower(i.position)
                agent.place_tower(TowerType.ICE_LUIGI, "3b", i.position)
        if agent.get_money(True) >= 3500:
            gen_init += 1

    #for general, mario
    if map_name == 'gen' and gen_init == 4:
        rx = random.randint(1, 14)
        ry = random.randint(1, 19)
        if agent.get_tower(True, Vector2(rx, ry)) == None and agent.get_terrain(Vector2(rx, ry)) == TerrainType.EMPTY:
            agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(rx, ry))
    #get_time
    remain_time = agent.get_remain_time()

    #get wave
    oldwave = wave
    wave = agent.get_current_wave()
    if wave != oldwave:
        print(f'now wave: {wave}')

    ###### tsai map ##########################################################
    tsai_init = 0
    # for tsai, put three pipes
    if coco_init == 0 and map_name == 'coco':
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 2))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 17))
        temp1 = agent.get_tower(True, Vector2(4, 2))
        temp2 = agent.get_tower(True, Vector2(7, 17))
        temp3 = agent.get_tower(True, Vector2(10, 17))
        if temp1 != None and temp2 != None and temp3 != None:##########start here
            coco_init += 1
            #print('tower is success')

    # for coco, after three pipes
    if coco_init == 1 and map_name == 'coco':
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 1))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(11, 7))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9, 8))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(3, 12))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(5, 12))
        agent.place_tower(TowerType.FORT, "1", Vector2(7, 19))
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 15))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 18))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 19))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 3))
        agent.place_tower(TowerType.FORT, "1", Vector2(10, 4))
        
        #check
        temp1 = agent.get_tower(True, Vector2(10, 17))
        temp2 = agent.get_tower(True, Vector2(10, 18))
        temp3 = agent.get_tower(True, Vector2(10, 19))
        temp4 = agent.get_tower(True, Vector2(7, 18))
        temp5 = agent.get_tower(True, Vector2(7, 19))
        temp6 = agent.get_tower(True, Vector2(4, 1))
        temp7 = agent.get_tower(True, Vector2(3, 12))
        temp8 = agent.get_tower(True, Vector2(5, 12))
        temp9 = agent.get_tower(True, Vector2(10, 3))
        temp10 = agent.get_tower(True, Vector2(10, 4))
        temp11 = agent.get_tower(True, Vector2(4, 15))
        temp12 = agent.get_tower(True, Vector2(11, 7))
        temp13 = agent.get_tower(True, Vector2(9, 8))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None and temp9 != None and temp10 != None and temp11 != None and temp12 != None and temp13 != None:
            coco_init += 1

    #for coco, Mairo
    if coco_init == 2 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(3, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(5, 14))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(6, 12))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(4, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 8))
        #check
        temp1 = agent.get_tower(True, Vector2(3, 13))
        temp2 = agent.get_tower(True, Vector2(5, 14))
        temp3 = agent.get_tower(True, Vector2(6, 12))
        temp4 = agent.get_tower(True, Vector2(9, 10))
        temp5 = agent.get_tower(True, Vector2(4, 15))
        temp6 = agent.get_tower(True, Vector2(11, 8))
        
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            coco_init += 1

    #for coco, remining da sing sing
    if coco_init == 3 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(5, 4))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(6, 4))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(8, 15))
        agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(9, 15))
        temp1 = agent.get_tower(True, Vector2(5, 4))
        temp2 = agent.get_tower(True, Vector2(6, 4))
        temp3 = agent.get_tower(True, Vector2(8, 15))
        temp4 = agent.get_tower(True, Vector2(9, 15))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None:
            coco_init += 1

    #for coco, ice
    if coco_init == 4 and map_name == 'coco':
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(3, 12))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 5))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(8, 9))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(5, 9))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(6, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(8, 14))
        agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(9, 14))
        #check
        temp1 = agent.get_tower(True, Vector2(3, 12))
        temp2 = agent.get_tower(True, Vector2(5, 5))
        temp3 = agent.get_tower(True, Vector2(8, 9))
        temp4 = agent.get_tower(True, Vector2(5, 9))
        temp5 = agent.get_tower(True, Vector2(6, 11))
        temp6 = agent.get_tower(True, Vector2(8, 14))
        temp7 = agent.get_tower(True, Vector2(9, 14))
        temp8 = agent.get_tower(True, Vector2(5, 11))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None:
            coco_init += 1

    

    #for coco, da sing sing & Mario ver.2
    if coco_init == 5 and map_name == 'coco':
        agent.place_tower(TowerType.DONKEY_KONG, "3b", Vector2(11, 6))
        agent.place_tower(TowerType.DONKEY_KONG, "3b", Vector2(12, 6))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(8, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(11, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(9, 8))
        temp1 = agent.get_tower(True, Vector2(11, 6))
        temp2 = agent.get_tower(True, Vector2(12, 6))
        temp3 = agent.get_tower(True, Vector2(8, 13))
        temp4 = agent.get_tower(True, Vector2(9, 13))
        temp5 = agent.get_tower(True, Vector2(11, 10))
        temp6 = agent.get_tower(True, Vector2(11, 11))
        temp7 = agent.get_tower(True, Vector2(9, 8))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None:
            coco_init += 1

    #for coco, last luan fang
    if coco_init == 6 and map_name == 'coco':
        x = 9
        for y in range(5, 16):
            temp1 = agent.get_tower(True, Vector2(x, y))
            if temp1 == None:
                if y % 3 == 0:
                    agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(x, y))
                elif y % 3 == 1:
                    agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(x, y))
                else:
                    agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(x, y))

        x = 11
        for y in range(6, 17):
            temp1 = agent.get_tower(True, Vector2(x, y))
            if temp1 == None:
                if y % 3 == 0:
                    agent.place_tower(TowerType.DONKEY_KONG, "3a", Vector2(x, y))
                elif y % 3 == 1:
                    agent.place_tower(TowerType.ICE_LUIGI, "3b", Vector2(x, y))
                else:
                    agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(x, y))
        
    #for ALL, double money spell
    if remain_time <= 270.0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    
    #for coco, teleport
    if map_name == 'coco':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.type == EnemyType.KOOPA:
                print('find koppa')
                #time.sleep(3)
                print('koppa pos: ', end = "")
                print(i.position)
                print(type(i.position))
                if i.position.x == 4:
                    if i.position.y == 19 or i.position.y == 18 or i.position.y == 17:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x, i.position.y -1))
                elif i.position.y == 16:
                    if i.position.x == 4 or i.position.x == 5 or i.position.x == 6:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x +1, i.position.y))

    #for coco, poison
    if map_name == 'coco':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.position.x == 10 and i.position.y == 5:
                agent.cast_spell(SpellType.POISON, Vector2(12, 5))
                break

    #for coco, li_bao_bao
    if loop_counter % 8 == 0 and coco_init >= 1 and coco_init <= 2 and map_name == 'coco':
        agent.spawn_unit(EnemyType.GOOMBA)
        #print('li bao bao success')
    
    #for general, li_bao_bao test
    if map_name == 'gen' and loop_counter % 5 == 0 and remain_time >= 210:
        agent.spawn_unit(EnemyType.GOOMBA)
        #print('li bao bao success')

    #for coco, flying turtles
    if coco_init >= 4 and map_name == 'coco':
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        print('flying turtle success')

    
    #get_time
    remain_time = agent.get_remain_time()

    #get wave
    oldwave = wave
    wave = agent.get_current_wave()
    if wave != oldwave:
        print(f'now wave: {wave}')    
    #get money
    #money = agent.get_money()
    
    
    ###### town map ##########################################################
    town_init = 0
    # for town, put two pipes
    if town_init == 0 and map_name == 'town':
        agent.place_tower(TowerType.FORT, "1", Vector2(13, 3))
        agent.place_tower(TowerType.FORT, "1", Vector2(12, 2))
        temp1 = agent.get_tower(True, Vector2(12, 2))
        temp2 = agent.get_tower(True, Vector2(13, 3))
        if temp1 != None and temp2 != None:
            town_init += 1
            print("wave 1, two pipes success")
            #print('tower is success')

    # for town, Mario
    if town_init == 1 and map_name == 'town':
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(11, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(11, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9,16 ))
        #check
        temp1 = agent.get_tower(True, Vector2(8, 16))
        temp2 = agent.get_tower(True, Vector2(9, 16))
        temp3 = agent.get_tower(True, Vector2(10, 16))
        temp4 = agent.get_tower(True, Vector2(11, 16))
        temp5 = agent.get_tower(True, Vector2(10, 15))
        temp6 = agent.get_tower(True, Vector2(11, 15))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            print('wave 2, Mario success')
            town_init += 1

    #for town, pipe ver.2
    if town_init == 2 and map_name == 'town':
        agent.place_tower(TowerType.FORT, "1", Vector2(13, 7))
        agent.place_tower(TowerType.FORT, "1", Vector2(1, 10))
        agent.place_tower(TowerType.FORT, "1", Vector2(13, 10))
        agent.place_tower(TowerType.FORT, "1", Vector2(14, 10))
        agent.place_tower(TowerType.FORT, "1", Vector2(13, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(14, 17))
        agent.place_tower(TowerType.FORT, "1", Vector2(4, 17))   
        #check
        temp1 = agent.get_tower(True, Vector2(13, 7))
        temp2 = agent.get_tower(True, Vector2(1, 10))
        temp3 = agent.get_tower(True, Vector2(13, 10))
        temp4 = agent.get_tower(True, Vector2(14, 10))
        temp5 = agent.get_tower(True, Vector2(13, 17))
        temp6 = agent.get_tower(True, Vector2(14, 17))
        temp7 = agent.get_tower(True, Vector2(4, 17))

        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None:
            print('wave 3, pipe ver.2 success')
            town_init += 1

    #for town, Mario ver.2
    if town_init == 3 and map_name == 'town':
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(4, 5))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(5, 6))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(6, 8))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(6, 9))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(7, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(7, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 14))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 14))
        temp1 = agent.get_tower(True, Vector2(4, 5))
        temp2 = agent.get_tower(True, Vector2(5, 6))
        temp3 = agent.get_tower(True, Vector2(6, 8))
        temp4 = agent.get_tower(True, Vector2(6, 9))
        temp5 = agent.get_tower(True, Vector2(7, 10))
        temp6 = agent.get_tower(True, Vector2(7, 11))
        temp7 = agent.get_tower(True, Vector2(8, 11))
        temp8 = agent.get_tower(True, Vector2(8, 13))
        temp9 = agent.get_tower(True, Vector2(8, 14))
        temp10 = agent.get_tower(True, Vector2(8, 15))
        temp11 = agent.get_tower(True, Vector2(9, 13))
        temp12 = agent.get_tower(True, Vector2(9, 15))
        temp13 = agent.get_tower(True, Vector2(10, 13))
        temp14 = agent.get_tower(True, Vector2(10, 14))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None and temp9 != None and temp10 != None and temp11 != None and temp12 != None and temp13 != None and temp14 !=  None:
            town_init += 1
            print('wave 4, Mario ver.2 success')
        

    # for town, Mario ver.3
    if town_init == 4 and map_name == 'town':
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(2, 14))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(3, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(4, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(5, 17))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(6, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(7, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(8, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(9, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(11, 18))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(12, 18))
        #check
        temp1 = agent.get_tower(True, Vector2(2, 14))
        temp2 = agent.get_tower(True, Vector2(3, 15))
        temp3 = agent.get_tower(True, Vector2(4, 16))
        temp4 = agent.get_tower(True, Vector2(5, 17))
        temp5 = agent.get_tower(True, Vector2(6, 18))
        temp6 = agent.get_tower(True, Vector2(7, 18))
        temp7 = agent.get_tower(True, Vector2(8, 18))
        temp8 = agent.get_tower(True, Vector2(9, 18))
        temp9 = agent.get_tower(True, Vector2(10, 18))
        temp10 = agent.get_tower(True, Vector2(11, 18))
        temp11 = agent.get_tower(True, Vector2(12, 18))

        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None and temp9 != None and temp10 != None and temp11 != None:
            print('wave 5, Mario ver.3 success')
            town_init += 1

  #for town, Luigi ver.1
    if town_init == 5 and map_name == 'town':
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(3, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(4, 12))
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(5, 13))
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(6, 14))
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(7, 15))
        agent.place_tower(TowerType.ICE_LUIGI, "1", Vector2(8, 16))
        #check
        temp1 = agent.get_tower(True, Vector2(3, 11))
        temp2 = agent.get_tower(True, Vector2(4, 12))
        temp3 = agent.get_tower(True, Vector2(5, 13))
        temp4 = agent.get_tower(True, Vector2(6, 14))
        temp5 = agent.get_tower(True, Vector2(7, 15))
        temp6 = agent.get_tower(True, Vector2(8, 16))

        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            print('wave 6, Luigi ver.1 success')
            town_init += 1
    '''   
    #for town, donkey ver.1
        if town_init == 6 and map_name == 'town':
            agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(7, 3))
            agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(9, 3))
            agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(11, 4))
            agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(11, 9))
            agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(9, 11))
            #check
            temp1 = agent.get_tower(True, Vector2(7, 3))
            temp2 = agent.get_tower(True, Vector2(9, 3))
            temp3 = agent.get_tower(True, Vector2(11, 4))
            temp4 = agent.get_tower(True, Vector2(11, 9))
            temp5 = agent.get_tower(True, Vector2(9, 11))

            if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None:
                town_init += 1
    '''
    #for town, ice
    if town_init == 6 and map_name == 'town':
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(11, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 16))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(11, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(9, 16))
        #check
        temp1 = agent.get_tower(True, Vector2(8, 16))
        temp2 = agent.get_tower(True, Vector2(11, 16))
        temp3 = agent.get_tower(True, Vector2(10, 15))
        temp4 = agent.get_tower(True, Vector2(10, 16))
        temp5 = agent.get_tower(True, Vector2(11, 15))
        temp6 = agent.get_tower(True, Vector2(9, 16))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            town_init += 1
    
        #for town, ice ver.2
    if town_init == 7 and map_name == 'town':
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(4, 5))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(5, 6))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(6, 8))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(6, 9))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(7, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(7, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 11))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 14))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(8, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(9, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(9, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 13))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 14))
        temp1 = agent.get_tower(True, Vector2(4, 5))
        temp2 = agent.get_tower(True, Vector2(5, 6))
        temp3 = agent.get_tower(True, Vector2(6, 8))
        temp4 = agent.get_tower(True, Vector2(6, 9))
        temp5 = agent.get_tower(True, Vector2(7, 10))
        temp6 = agent.get_tower(True, Vector2(7, 11))
        temp7 = agent.get_tower(True, Vector2(8, 11))
        temp8 = agent.get_tower(True, Vector2(8, 13))
        temp9 = agent.get_tower(True, Vector2(8, 14))
        temp10 = agent.get_tower(True, Vector2(8, 15))
        temp11 = agent.get_tower(True, Vector2(9, 13))
        temp12 = agent.get_tower(True, Vector2(9, 15))
        temp13 = agent.get_tower(True, Vector2(10, 13))
        temp14 = agent.get_tower(True, Vector2(10, 14))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None and temp7 != None and temp8 != None and temp9 != None and temp10 != None and temp11 != None and temp12 != None and temp13 != None and temp14 != None:
            coco_init += 1
   
    #for town, ice ver.3
    if town_init == 8 and map_name == 'town':
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(3, 11))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(4, 12))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(5, 13))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(6, 14))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(7, 15))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(8, 16))
        temp1 = agent.get_tower(True, Vector2(3, 11))
        temp2 = agent.get_tower(True, Vector2(4, 12))
        temp3 = agent.get_tower(True, Vector2(5, 13))
        temp4 = agent.get_tower(True, Vector2(6, 14))
        temp5 = agent.get_tower(True, Vector2(7, 15))
        temp6 = agent.get_tower(True, Vector2(8, 16))
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            town_init += 1
           
     
    #for town, double money spell
    if map_name == 'town' and town_init >= 1:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    

    #for town, teleport
    if map_name == 'town':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.type == EnemyType.KOOPA:
                print('find koppa')
                #time.sleep(3)
                print('koppa pos: ', end = "")
                print(i.position)
                print(type(i.position))
                if i.position.x == 6:
                    if i.position.y == 10 or i.position.y == 11 or i.position.y == 12:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x, i.position.y -1))
                elif i.position.y == 17:
                    if i.position.x == 8 or i.position.x == 9 or i.position.x == 10:
                        print('at correct pos')
                        agent.cast_spell(SpellType.TELEPORT, Vector2(i.position.x +1, i.position.y))

    #for town, poison
    if map_name == 'town':
        enemylist = agent.get_all_enemies(True)
        for i in enemylist:
            if i.position.x == 2 and i.position.y == 12:
                agent.cast_spell(SpellType.POISON, Vector2(2, 12))
                break
    
    #for town, li_bao_bao
    if loop_counter % 6 == 0 and town_init >= 1 and town_init <= 2 and map_name == 'town':
        agent.spawn_unit(EnemyType.GOOMBA)
        print('li bao bao success')
    
    ##################space_map#################
    space_init = 0
    
    if space_init == 0 and map_name == 'space':

        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(10, 9))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(12, 12))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(6, 15))
        agent.place_tower(TowerType.FIRE_MARIO, "1", Vector2(7, 15))

        temp1 = agent.get_tower(True, Vector2(10, 9))
        temp2 = agent.get_tower(True, Vector2(12, 12))
        temp3 = agent.get_tower(True, Vector2(6, 15))
        temp4 = agent.get_tower(True, Vector2(7, 15))
        
        if temp1 != None and temp2 != None and temp3 != None and temp4 != None :
            space_init += 1
            #print('tower is success')


    #for space spawn don ki kong + lu yi ji
    if map_name == "space" and space_init == 1:

        agent.place_tower(TowerType.DONKEY_KONG, "1", Vector2(7, 4))
        agent.place_tower(TowerType.DONKEY_KONG, "1", Vector2(8, 15))


        temp1 = agent.get_tower(True, Vector2(7, 4))
        temp2 = agent.get_tower(True, Vector2(8, 15))

        if temp1 != None and temp2 != None:
            space_init += 1
            #print('tower is success')

    if map_name == "space" and space_init == 2:
        agent.place_tower(TowerType.DONKEY_KONG, "1", Vector2(3, 2))
        agent.place_tower(TowerType.DONKEY_KONG, "1", Vector2(7, 13))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(9, 4))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(6, 6))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(6, 7))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(8, 13))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(11, 10))

        temp1 = agent.get_tower(True, Vector2(3, 2))
        temp2 = agent.get_tower(True, Vector2(7, 13))    
        temp3 = agent.get_tower(True, Vector2(9, 4)) 
        temp4 = agent.get_tower(True, Vector2(6, 6))
        temp5 = agent.get_tower(True, Vector2(6, 7))
        temp6 = agent.get_tower(True, Vector2(8, 13)) 
        temp7 = agent.get_tower(True, Vector2(11, 10)) 

        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5  != None and temp6 != None and temp7 != None :
            space_init += 1
            #print('tower is success')



    if map_name == "space" and space_init == 3:
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(6, 16))
        agent.place_tower(TowerType.DONKEY_KONG, "2a", Vector2(8, 15))

        temp3 = agent.get_tower(True, Vector2(6, 16))
        temp4 = agent.get_tower(True, Vector2(8, 15))

        if temp3 != None and temp4 != None :
            space_init += 1
            #print('tower is success')
    
    #for space spawn li bao bao
    if loop_counter%4==0 and  space_init >= 1 and map_name =="space":
        agent.spawn_unit(EnemyType.GOOMBA)
        #print('li bao bao success')

    if map_name == 'space' and space_init >= 1 :
        agent.cast_spell(SpellType.DOUBLE_INCOME,Vector2(1,1))
    
    if map_name == "space" and space_init == 4:

        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(11, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(13, 8))
        agent.place_tower(TowerType.ICE_LUIGI, "2b", Vector2(13, 9))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(13, 10))
        agent.place_tower(TowerType.FIRE_MARIO, "2a", Vector2(10, 11))

        temp1 = agent.get_tower(True, Vector2(11, 10))
        temp2 = agent.get_tower(True, Vector2(10, 10))
        temp3 = agent.get_tower(True, Vector2(13, 8))
        temp4 = agent.get_tower(True, Vector2(13, 9))
        temp5 = agent.get_tower(True, Vector2(13, 10))
        temp6 = agent.get_tower(True, Vector2(10, 11))

        if temp1 != None and temp2 != None and temp3 != None and temp4 != None and temp5 != None and temp6 != None:
            space_init += 1
            #print('tower is success')
    
    if map_name == "space" and space_init == 5:
        for x in range(6,14):
            for y in range(6, 19):
                temp1 = agent.get_tower(True, Vector2(x, y))
                if temp1 == None:
                    agent.place_tower(TowerType.FIRE_MARIO, "3a", Vector2(x, y))
        space_init +=1
    
        

    ############################################
    
    '''
    #for town, flying turtles
    if town_init >= 4 and map_name == 'town':
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        print('flying turtle success')

    '''
    """
    # CAST DOUBLE INCOME
    income_multiplier: int = 1
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    income_multiplier = 2
    
    # INCOME ENHANCEMENT
    if agent.get_income(True) / income_multiplier < 150:
        agent.spawn_unit(EnemyType.GOOMBA)
    elif len(agent.get_all_towers(True)) > 20 and agent.get_income(True) / income_multiplier < 250:
        agent.spawn_unit(EnemyType.GOOMBA)
    
    # DEFENSE
    terrain = agent.get_all_terrain()
    for (row, data) in enumerate(terrain):
        for (col, tile) in enumerate(data):
            if tile == TerrainType.EMPTY:
                agent.place_tower(TowerType.FIRE_MARIO, '1', Vector2(row, col))
    
    # ATTACK
    if agent.get_money(True) >= 3000:
        agent.spawn_unit(EnemyType.KOOPA_JR)

    # CHAT
    agent.send_chat('你說飛行敵人太強，其實是你太習慣凡事都想一步解決。')
    """
    
