# Copyright © 2025 mtmatt, ouo. All rights reserved.

import time, copy, numpy
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource


agent = GameClient(7749, "50ef3715")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

SYSTEM_RATIO = 1
PLAYER_RATIO = 0.7
GROUND_RATIO = 1
AIR_RATIO = 0.35

ground_system_path = [ (c.x, c.y) for c in agent.get_system_path(False) ]
air_system_path = [ (c.x, c.y) for c in agent.get_system_path(True) ]
ground_player_path = [ (c.x, c.y) for c in agent.get_opponent_path(False) ]
air_player_path = [ (c.x, c.y) for c in agent.get_opponent_path(True) ]

# air_system_path = agent.get_system_path(True)
# ground_player_path = agent.get_opponent_path(False)
# air_player_path = agent.get_opponent_path(True)
terrain = agent.get_all_terrain()

def fort_count(pos: Vector2):
    global ground_system_path, air_system_path, ground_player_path, air_player_path, terrain
    # print(ground_system_path, air_system_path, ground_player_path, air_player_path)
    ground_count, air_count, road, dx, dy = 0, 0, 0, 1, 0
    for _ in range(4):
        count1, count2, count_road = 0, 0, 0
        for j in range(20):
            if pos.x + dx * j < 0 or pos.x + dx * j >= len(terrain) or pos.y + dy * j < 0 or pos.y + dy * j >= len(terrain[0]):
                break
            if terrain[pos.x + dx * j][pos.y + dy * j] == TerrainType.ROAD:
                count_road += 1
            if (pos.x + dx * j, pos.y + dy * j) in ground_system_path:
                count1 += GROUND_RATIO * SYSTEM_RATIO
            if (pos.x + dx * j, pos.y + dy * j) in ground_player_path:
                count1 += GROUND_RATIO * PLAYER_RATIO
            if (pos.x + dx * j, pos.y + dy * j) in air_system_path:
                count2 += AIR_RATIO * SYSTEM_RATIO
            if (pos.x + dx * j, pos.y + dy * j) in air_player_path:
                count2 += AIR_RATIO * PLAYER_RATIO
        print(pos, ":", count_road, count1, count2)
        if road < count_road:
            road, ground_count, air_count = count_road, count1, count2
        dx, dy = -dy, dx
    if 500 * (1 - 1 / 2 ** ground_count) > 20 * (ground_count + air_count):
        return (350 * (1 - 1 / 2 ** ground_count), "2a")
    return (60 * (ground_count + air_count) / 2, "2b")

def ice_count(pos: Vector2):
    global ground_system_path, air_system_path, ground_player_path, air_player_path, terrain
    ground_count, air_count = 0, 0
    for i in range(-3, 3):
        for j in range(-3, 3):
            if pos.x + i < 0 or pos.x + i >= len(terrain) or pos.y + j < 0 or pos.y + j >= len(terrain[0]) or 50 * (i ** 2 + j ** 2) > 200:
                continue
            if (pos.x + i, pos.y + j) in ground_system_path:
                ground_count += GROUND_RATIO * SYSTEM_RATIO
            if (pos.x + i, pos.y + j) in ground_player_path:
                ground_count += GROUND_RATIO * PLAYER_RATIO
            if (pos.x + i, pos.y + j) in air_system_path:
                air_count += AIR_RATIO * SYSTEM_RATIO
            if (pos.x + i, pos.y + j) in air_player_path:
                air_count += AIR_RATIO * PLAYER_RATIO
    return (ground_count + air_count * 3.5)

best, ord = {}, []

def best_tower():
    for (row, data) in enumerate(terrain):
        for (col, tile) in enumerate(data):
            if tile == TerrainType.EMPTY:
                val, tp = fort_count(Vector2(row, col))
                print(f"({row}, {col}) val: {val:.2f} tp: {tp}")
                if val < 335:
                    ival = ice_count(Vector2(row, col))
                    # if ival > 3.5:
                    #     best[(row, col)] = (TowerType.ICE_LUIGI, "2b")
                    #     ord.append((TowerType.ICE_LUIGI, "2b", ival, (row, col), 1200))
                    if ival > 0:
                        best[(row, col)] = (TowerType.FIRE_MARIO, "1")
                        ord.append((TowerType.FIRE_MARIO, "1", ival, (row, col), 400))
                else:
                    best[(row, col)] = (TowerType.FORT, tp)
                    ord.append((TowerType.FORT, tp, val, (row, col), 1200))

best_tower()

for row in terrain:
    for t in row:
        print(f"{t.value:2d}", end=" ")
    print()
print()

for (row, data) in enumerate(terrain):
    for (col, tile) in enumerate(data):
        if (row, col) in best:
            print(f"{best[(row, col)][0]}", end=" ")
        else:
            print("0", end=" ")
    print()

ord.sort(key=lambda x: (x[0].value, x[2]))
print("\nSorted order:", ord)
ord.reverse()
# # 1. 地形
# terrain = agent.get_all_terrain()
# for row in terrain:
#     for t in row:
#         print(f"{t.value:2d}", end=" ")
#     print()
# print("Single terrain at (4,4):", agent.get_terrain(Vector2(4, 4)), "\n")

# 2. 分數、金錢、收入
print("Scores:", agent.get_scores(True), "(Me) /", agent.get_scores(False), "(Opp)")
print("Money: ", agent.get_money(True), "(Me) /", agent.get_money(False), "(Opp)")
print("Income:", agent.get_income(True), "(Me) /", agent.get_income(False), "(Opp)\n")

# 3. 波次與時間
print("Wave:", agent.get_current_wave())
print("Remain time:", f"{agent.get_remain_time():.2f}s")
print("Until next wave:", f"{agent.get_time_until_next_wave():.2f}s\n")

# 4. 路徑
# print("System path (ground):", [(c.x, c.y) for c in agent.get_system_path(False)])
# print("Opponent path (air):",  [(c.x, c.y) for c in agent.get_opponent_path(True)], "\n")

# 5. 塔操作
# pos = Vector2(5, 5)
# if agent.get_tower(True, pos) is None:
#     print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
#     agent.place_tower(TowerType.FIRE_MARIO, "1", pos)
# print("All my towers:", agent.get_all_towers(True))
# # 設定塔的攻擊模式
# agent.set_strategy(pos, TargetStrategy.CLOSE)

# if agent.get_tower(True, Vector2(1, 2)) is None:
#     agent.place_tower(TowerType.ICE_LUIGI, "1", pos)
# time.sleep(3)
# 賣塔
# agent.sell_tower(Vector2(1, 1))
# print("After sell:", agent.get_all_towers(True), "\n")

# 6. 出兵
agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
print("Opp enemies:", agent.get_all_enemies(False))
print("KOOPA cooldown:", f"{agent.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA):.2f}s\n")

# 7. 法術
# agent.cast_spell(SpellType.POISON, Vector2(3, 3))
# print("My POISON CD:", f"{agent.get_spell_cooldown(True, SpellType.POISON):.2f}s\n")

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

possible = [0, 0.7, 0, 0, 0.3, 0]
next, ok = 4, 0

while True:
    remain_time = agent.get_remain_time()
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    agent.cast_spell(SpellType.POISON, Vector2(ground_system_path[2][0], ground_system_path[2][1]))
    
    if agent.get_income(True) < 150 and len(agent.get_all_towers(True)) > 2:
        agent.spawn_unit(EnemyType.GOOMBA)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    elif len(agent.get_all_towers(True)) > 25 and agent.get_income(True) < 250:
        agent.spawn_unit(EnemyType.GOOMBA)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        agent.spawn_unit(EnemyType.BUZZY_BEETLE)
    elif len(agent.get_all_towers(True)) > 45 and agent.get_income(True) < 500:
        agent.spawn_unit(EnemyType.GOOMBA)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    elif len(agent.get_all_towers(True)) > 65 and agent.get_income(True) < 700:
        agent.spawn_unit(EnemyType.GOOMBA)
        agent.spawn_unit(EnemyType.KOOPA_JR)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    elif len(agent.get_all_towers(True)) > 85:
        agent.spawn_unit(EnemyType.GOOMBA)
        agent.spawn_unit(EnemyType.KOOPA_JR)
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    for (tower_type, tower_level, val, pos, tower_cost) in ord:
        if agent.get_tower(True, Vector2(*pos)) is None and tower_type == next:
            if agent.get_money(True) >= tower_cost:
                agent.place_tower(tower_type, tower_level, Vector2(*pos))
                next = numpy.random.choice([0, 1, 2, 3, 4, 5], p=possible)
            else:
                ok = 1
            break
    
    if ok == 0:
        next = numpy.random.choice([0, 1, 2, 3, 4, 5], p=possible)

            # if agent.get_money(True) >= tower_cost:
            #     agent.place_tower(tower_type, tower_level, Vector2(*pos))
            # else:
            #     break

    # ATTACK
    if agent.get_money(True) >= 3000:
        agent.spawn_unit(EnemyType.KOOPA_JR)

    # CHAT
    agent.send_chat('你說飛行敵人太強，其實是你太習慣凡事都想一步解決。')