import time
from api import *

api = GameClient(7749, "8604d67d") # Replace with your own port and token

print("Waiting for game to RUNNING...")
while api.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

# 1. 地形
terrain = api.get_all_terrain()
for row in terrain:
    for t in row:
        print(f"{t.value:2d}", end=" ")
    print()
print("Single terrain at (4,4):", api.get_terrain(Vector2(4, 4)), "\n")

# 2. 分數、金錢、收入
print("Scores:", api.get_scores(True), "(Me) /", api.get_scores(False), "(Opp)")
print("Money: ", api.get_money(True), "(Me) /", api.get_money(False), "(Opp)")
print("Income:", api.get_income(True), "(Me) /", api.get_income(False), "(Opp)\n")

# 3. 波次與時間
print("Wave:", api.get_current_wave())
print("Remain time:", f"{api.get_remain_time():.2f}s")
print("Until next wave:", f"{api.get_time_until_next_wave():.2f}s\n")

# 4. 路徑
print("System path (ground):", [(c.x, c.y) for c in api.get_system_path(False)])
print("Opponent path (air):",  [(c.x, c.y) for c in api.get_opponent_path(True)], "\n")

# 5. 塔操作
pos = Vector2(5, 5)
if api.get_tower(True, pos) is None:
    print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
    api.place_tower(TowerType.FIRE_MARIO, "1", pos)
print("All my towers:", api.get_all_towers(True))
#設定塔的攻擊模式
api.set_strategy(pos, TargetStrategy.CLOSE)

if api.get_tower(True, Vector2(1, 2)) is None:
    api.place_tower(TowerType.ICE_LUIGI, "1", pos)
time.sleep(3)
#賣塔
api.sell_tower(Vector2(1, 1))
print("After sell:", api.get_all_towers(True), "\n")

# 6. 出兵
api.spawn_unit(EnemyType.KOOPA_PARATROOPA)
print("Opp enemies:", api.get_all_enemies(False))
print("KOOPA cooldown:", f"{api.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA):.2f}s\n")

# 7. 法術
api.cast_spell(SpellType.POISON, Vector2(3, 3))
print("My POISON CD:", f"{api.get_spell_cooldown(True, SpellType.POISON):.2f}s\n")

# 8. 聊天
api.set_name("OuO")
api.set_chat_name_color("DCB5FF")
sent = api.send_chat("OuO love you ! <3")
history = api.get_chat_history(5)
for src, msg in history:
    if src == ChatSource.PLAYER_SELF:
        who = "OuO"
    elif src == ChatSource.PLAYER_OTHER:
        who = "Loser"
    else:
        who = "System"
    print(f"[{who}]", msg)
print()

# 9. 其他
# print("Pixel Cat:\n", api.pixelcat())
# print("Developers:", api.get_devs())

while True:
    #place tower everywhere
    for x in range(15):
        for y in range(15):
            pos = Vector2(x, y)
            if api.get_tower(True, pos) is None:
                api.send_chat("OuO <3")
                api.place_tower(TowerType.ICE_LUIGI, "1", pos)
            
