# Copyright © 2025 mtmatt, ouo. All rights reserved.

import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

agent = GameClient(7749, "67ec39f2")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

for i in range(10):
    print(agent.spam("i use arch btw", 96, "#ff69b4"))
    time.sleep(0.5)
    print(agent.spam("i use arch btw", 48))
    time.sleep(0.5)
# 1. 地形
#terrain = agent.get_all_terrain()
#for row in terrain:
#    for t in row:
#        print(f"{t.value:2d}", end=" ")
#    print()
#print("Single terrain at (4,4):", agent.get_terrain(Vector2(4, 4)), "\n")
#
## 2. 分數、金錢、收入
#print("Scores:", agent.get_scores(True), "(Me) /", agent.get_scores(False), "(Opp)")
#print("Money: ", agent.get_money(True), "(Me) /", agent.get_money(False), "(Opp)")
#print("Income:", agent.get_income(True), "(Me) /", agent.get_income(False), "(Opp)\n")
#
## 3. 波次與時間
#print("Wave:", agent.get_current_wave())
#print("Remain time:", f"{agent.get_remain_time():.2f}s")
#print("Until next wave:", f"{agent.get_time_until_next_wave():.2f}s\n")
#
## 4. 路徑
#print("System path (ground):", [(c.x, c.y) for c in agent.get_system_path(False)])
#print("Opponent path (air):",  [(c.x, c.y) for c in agent.get_opponent_path(True)], "\n")
#
## 5. 塔操作
#pos = Vector2(5, 5)
#if agent.get_tower(True, pos) is None:
#    print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
#    agent.place_tower(TowerType.FIRE_MARIO, "1", pos)
#print("All my towers:", agent.get_all_towers(True))
## 設定塔的攻擊模式
#agent.set_strategy(pos, TargetStrategy.CLOSE)
#
#if agent.get_tower(True, Vector2(1, 2)) is None:
#    agent.place_tower(TowerType.ICE_LUIGI, "1", pos)
#time.sleep(3)
## 賣塔
#agent.sell_tower(Vector2(1, 1))
#print("After sell:", agent.get_all_towers(True), "\n")
#
## 6. 出兵
#agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
#print("Opp enemies:", agent.get_all_enemies(False))
#print("KOOPA cooldown:", f"{agent.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA):.2f}s\n")
#
## 7. 法術
#agent.cast_spell(SpellType.POISON, Vector2(3, 3))
#print("My POISON CD:", f"{agent.get_spell_cooldown(True, SpellType.POISON):.2f}s\n")
#
## 8. 聊天
#agent.set_name("OuO")
#agent.set_chat_name_color("DCB5FF")
#sent = agent.send_chat("OuO love you ! <3")
#history = agent.get_chat_history(5)
#for src, msg in history:
#    if src == ChatSource.PLAYER_SELF:
#        who = "OuO"
#    elif src == ChatSource.PLAYER_OTHER:
#        who = "Loser"
#    else:
#        who = "System"
#    print(f"[{who}]", msg)
#print()
#
#
#while True:
#    remain_time = agent.get_remain_time()
#
#    # CAST DOUBLE INCOME
#    income_multiplier: int = 1
#    agent.cast_spell(SpellType.DOUBLE_INCOME)
#    income_multiplier = 2
#
#    # INCOME ENHANCEMENT
#    if agent.get_income(True) / income_multiplier < 150:
#        agent.spawn_unit(EnemyType.GOOMBA)
#    elif len(agent.get_all_towers(True)) > 20 and agent.get_income(True) / income_multiplier < 250:
#        agent.spawn_unit(EnemyType.GOOMBA)
#
#    # DEFENSE
#    terrain = agent.get_all_terrain()
#    for (row, data) in enumerate(terrain):
#        for (col, tile) in enumerate(data):
#            if tile == TerrainType.EMPTY:
#                agent.place_tower(TowerType.FIRE_MARIO, '1', Vector2(row, col))
#
#    # ATTACK
#    if agent.get_money(True) >= 3000:
#        agent.spawn_unit(EnemyType.KOOPA_JR)
#
#    # CHAT
#    agent.send_chat('你說飛行敵人太強，其實是你太習慣凡事都想一步解決。')
