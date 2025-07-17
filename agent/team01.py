# Copyright © 2025 mtmatt, ouo. All rights reserved.
from random import randint
from api import TerrainType, TowerType, Vector2
import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource
import math
agent = GameClient(7749, "f6ca504b")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

agent.set_chat_name_color("7fffd4")
agent.set_name("poyo")

placed_dk = set()
placed_luigi = set()
# 1. 地形
# this need to be flipped and turn clockwise
terrain = agent.get_all_terrain()
'''
for row in terrain:
    for t in row:
        print(f"{t.value:2d}", end=" ")
    print()
'''

# fly path
fly_path = agent.get_system_path(True)


def find_best_donkey_kong_position(terrain, min_road_tiles=8):
    """
    Find all possible DK tower spots using a 4x4 range.

    :param terrain: result of agent.get_all_terrain()
    :param min_road_tiles: minimum roads required to consider a tile
    :return: list of tuples (Vector2, road_count), sorted descending
    """

    rows = len(terrain)
    cols = len(terrain[0])

    spots = []

    for r in range(rows):
        for c in range(cols):
            if terrain[r][c] != TerrainType.EMPTY:
                continue

            road_count = 0

            for dr in range(-2, 3):  # -2 to +2
                for dc in range(-2, 3):
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < rows and 0 <= nc < cols:
                        if terrain[nr][nc] == TerrainType.ROAD:
                            road_count += 1

            if road_count >= min_road_tiles:
                spots.append((Vector2(r, c), road_count))

    # Sort by highest road count
    spots.sort(key=lambda x: x[1], reverse=True)

    return spots


def find_corner(terrain):

    # direction definition

    DIRS = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1),  # right
    ]
    # Find corners. ex DIRS[0] + DIRS[2] = up + left
    CORNER_PAIRS = [
        (0, 2),  # up + left
        (0, 3),  # up + right
        (1, 2),  # down + left
        (1, 3),  # down + right
    ]
    corner_positions = []

    rows = len(terrain)
    cols = len(terrain[0])

    for row in range(rows):
        for col in range(cols):
            if terrain[row][col] == TerrainType.EMPTY:
                for a, b in CORNER_PAIRS:
                    row_a, col_a = row + DIRS[a][0], col + DIRS[a][1]
                    row_b, col_b = row + DIRS[b][0], col + DIRS[b][1]

                    # Check bounds
                    if not (0 <= row_a < rows and 0 <= col_a < cols):
                        continue
                    if not (0 <= row_b < rows and 0 <= col_b < cols):
                        continue

                    if (terrain[row_a][col_a] == TerrainType.ROAD and
                            terrain[row_b][col_b] == TerrainType.ROAD):
                        corner_positions.append(Vector2(row, col))
                        break  # No need to check other pairs
    # Check single terrain and corner positions
    # print("Single terrain at (0,0):", agent.get_terrain(Vector2(0, 0)), "\n")
    # X is down, Y is right
    # print("\nCorners found:")
    # for pos in corner_positions:
    # print(f"Corner at: ({pos.x}, {pos.y})")
    return corner_positions


# mario.py
def place_mario_4x4_on_fly_path(agent, terrain, level="1"):
    """
    Tries to place a 4x4 block of FIRE_MARIO towers along the flying path, starting from the back.

    :param agent: GameClient
    :param terrain: result of agent.get_all_terrain()
    :param level: tower level (e.g. "1", "2a")
    """

    fly_path = agent.get_system_path(True)[::-1]  # from the back
    rows = len(terrain)
    cols = len(terrain[0])

    for center in fly_path:
        cx, cy = center.x, center.y

        # Try placing 4x4 block with top-left at (cx, cy)
        can_place = True
        block_positions = []

        for dx in range(4):
            for dy in range(4):
                x = cx + dx
                y = cy + dy

                if not (0 <= x < cols and 0 <= y < rows):
                    can_place = False
                    break

                pos = Vector2(x, y)
                if terrain[y][x] != TerrainType.EMPTY:
                    can_place = False
                    break
                if agent.get_tower(True, pos) is not None:
                    can_place = False
                    break

                block_positions.append(pos)

            if not can_place:
                break

        if can_place:
            for pos in block_positions:
                agent.place_tower(TowerType.FIRE_MARIO, level, pos)
                print(f"Placed FIRE_MARIO level {level} at {pos} (4x4 block)")
            return

    print("No suitable 4x4 block found along flying path for FIRE_MARIO.")


def place_mario_for_flyers(agent, terrain, fly_path, level="2", num_towers=3):
    """
    Places FIRE_MARIO towers along the flying path, starting from the back.

    :param agent: GameClient instance
    :param level: Mario tower level, e.g. "1", "2a"
    :param num_towers: how many towers to place
    """

    fly_path = agent.get_system_path(True)
    fly_path_reversed = fly_path[::-1]

    placed = 0

    for pos in fly_path_reversed:
        terrain_type = agent.get_terrain(pos)

        if terrain_type == TerrainType.EMPTY:
            tower = agent.get_tower(True, pos)
            if tower is None:
                agent.place_tower(TowerType.FIRE_MARIO, "2a", pos)
                print(
                    f"Placed FIRE_MARIO level {level} at {pos} (air defense).")
                placed += 1

            if placed >= num_towers:
                break
                placed = 0

    if placed == 0:
        print("No suitable tiles found to place FIRE_MARIO towers.")


def get_mario_spots_3x3(agent, terrain):
    """
    Returns a list of all EMPTY, unoccupied tiles within a 3×3 block
    centered on each flying-path tile (back→front order).

    :param agent: GameClient
    :param terrain: result of agent.get_all_terrain()
    :return: list of Vector2 positions
    """
    fly_path = agent.get_system_path(True)[::-1]  # from end back to start
    rows = len(terrain)
    cols = len(terrain[0])

    spots = []
    seen = set()  # to avoid duplicates

    for center in fly_path:
        cx, cy = center.x, center.y
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                x = cx + dx
                y = cy + dy

                # bounds check
                if not (0 <= x < cols and 0 <= y < rows):
                    continue

                key = (x, y)
                if key in seen:
                    continue

                # must be empty and no tower there yet
                if terrain[y][x] != TerrainType.EMPTY:
                    continue
                if agent.get_tower(True, Vector2(x, y)) is not None:
                    continue

                seen.add(key)
                spots.append(Vector2(x, y))

    return spots


def get_5x5_positions_on_all_paths(agent, terrain):
    """
    Returns all unique Vector2 positions in a 5x5 area centered on
    both flying and ground path tiles.

    :param agent: GameClient
    :param terrain: result of agent.get_all_terrain()
    :return: list of Vector2 positions
    """

    rows = len(terrain)
    cols = len(terrain[0])

    fly_path = agent.get_system_path(True)
    ground_path = agent.get_system_path(False)

    all_path = fly_path + ground_path
    seen = set()
    positions = []

    for tile in all_path:
        cx, cy = tile.x, tile.y

        for dx in range(-2, 3):  # -2 to 2
            for dy in range(-2, 3):
                x = cx + dx
                y = cy + dy

                if 0 <= x < cols and 0 <= y < rows:
                    key = (x, y)
                    if key not in seen:
                        seen.add(key)
                        positions.append(Vector2(x, y))

    return positions


def get_positions_around(pos: Vector2, terrain, radius=1):
    """
    Returns a list of Vector2 tiles in a square radius around a center position.

    :param pos: center Vector2
    :param terrain: result of agent.get_all_terrain()
    :param radius: 1 = 3x3, 2 = 5x5, etc.
    """
    rows = len(terrain)
    cols = len(terrain[0])
    cx, cy = pos.x, pos.y

    positions = []

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            x = cx + dx
            y = cy + dy

            if 0 <= x < cols and 0 <= y < rows:
                positions.append(Vector2(x, y))

    return positions


terrain = agent.get_all_terrain()
fly_path = agent.get_system_path(True)
end_tile = fly_path[-1]

around_end = get_positions_around(end_tile, terrain, radius=1)


mario_spots = get_mario_spots_3x3(agent, terrain)
luigi2_spots = get_mario_spots_3x3(agent, terrain)
dk2_spots = get_5x5_positions_on_all_paths(agent, terrain)
# find corners
corner_positions = find_corner(terrain)
luigi_spots = corner_positions
start_enemy = False
# print("Flying enemy path:")

# for coord in fly_path:
#    print(f"({coord.x}, {coord.y})")
dk_start = 0
luigi_time = False
dk_a_amount = 0
dk_b_amount = 0
mario_a_amount = 0
mario_b_amount = 0

flyers_last_check_time = 0
koopa_last_check_time = 0
while True:  # 主遊戲
    remain_time = agent.get_remain_time()
    now = 300 - remain_time  # 紀錄現在時間

    # agent.send_chat('start-process powershell –verb runAs')

    agent.set_the_radiant_core_of_stellar_faith(3037)
    # agent.get_the_radiant_core_of_stellar_faith()
    # dk best position
    dk_spots = find_best_donkey_kong_position(terrain)
    # print(dk_spots)
    all_my_towers = agent.get_all_towers(True)

    mario_a_amount = sum(
        1 for t in all_my_towers if t.type == TowerType.FIRE_MARIO)

    dk_b_towers = [
        t for t in all_my_towers
        if t.type == TowerType.DONKEY_KONG and t.level_b > t.level_a
    ]
    # print(f"Current Mario A amount: {mario_a_amount}")
    # all_enemies = agent.get_all_enemies(True)  # 獲取自己地圖上所有敵人的資訊
    # print(all_enemies)

    # monster spawn
    if now >= 0 and start_enemy:
        agent.spawn_unit(EnemyType.GOOMBA)

    turtles_lastCheckTime = 0
    if now >= 180 and (now - turtles_lastCheckTime) >= 2:
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    if now >= 240 and (now - turtles_lastCheckTime) >= 2:
        putNum = randint(1, 3)
        if putNum == 1:
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        elif putNum == 2:
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
        else:
            agent.spawn_unit(EnemyType.SPINY_SHELL)
        turtles_lastCheckTime = now
    # spell  cast
    lastCheckTime = 0
    checkTime = 0
    # teleport
    transCool = agent.get_spell_cooldown(True, SpellType.TELEPORT)
    if transCool == 0 and now <= 120:
        enemys = agent.get_all_enemies(True)
        key = randint(0, len(enemys)-1)
        transpos = enemys[key].position
        agent.cast_spell(SpellType.TELEPORT, (transpos))

    if transCool == 0 and now > 180:
        target = 'KOOPA.JR'
        enemys = agent.get_all_enemies(True)
        positions = [
            enemy.position for enemy in enemys if enemy.type == target]
        agent.cast_spell(SpellType.TELEPORT, (positions))
    if transCool == 0 and now > 240:
        target = 'KOOPA'
        enemys = agent.get_all_enemies(True)
        positions = [
            enemy.position for enemy in enemys if enemy.type == target]
        agent.cast_spell(SpellType.TELEPORT, (positions))
    # poison
    spellCooldown = agent.get_spell_cooldown(True, SpellType.POISON)
    if spellCooldown == 0:
        position = agent.get_system_path(True)
        posPosition = position[-1]
        print(f"Poisoning at {posPosition}")
        agent.cast_spell(SpellType.POISON, (posPosition))

    # spell db cast
    DOUBLE_INCOME_first_usage = False
    if now >= 20:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
        agent.send_chat('兩倍錢>:)')
        DOUBLE_INCOME_first_usage = True
    if agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) == 0 and DOUBLE_INCOME_first_usage == True:  # 兩倍錢
        agent.cast_spell(SpellType.DOUBLE_INCOME)
        agent.send_chat('兩倍錢>:)')

    # dk1
    if agent.get_money(True) >= 1200 and dk_a_amount < 9:
        for pos in dk_spots:
            if agent.get_tower(True, pos[0]) is None and dk_a_amount < 10:
                print(f"Placing DK at {pos[0]}")
                agent.place_tower(TowerType.DONKEY_KONG, '2a', pos[0])
                agent.send_chat('放置lv 2 DK')
                dk_a_amount += 1
                dk_spots.remove(pos)
                start_enemy = True
                break
    # dk2_high dmg
    if agent.get_money(True) >= 2900 and now >= 100 and dk_b_amount < 10 and dk_a_amount + mario_a_amount >= 15:
        print("dk2 start")
        for dk2_spot in dk2_spots:
            print(f"Checking DK2 spot: {dk2_spot}")
            if agent.get_tower(True, dk2_spot) is None and dk_b_amount < 10:
                print(f"Placing DK at {dk2_spot}")
                agent.place_tower(TowerType.DONKEY_KONG, '3b', dk2_spot)
                agent.send_chat('放置lv 2 DK')
                dk_b_amount += 1
                dk2_spots.remove(dk2_spot)
                start_enemy = True
                break
    # mario start
    if now >= 0:
        for mario_spot in mario_spots:
            if agent.get_money(True) >= 1400 and agent.get_tower(True, mario_spot) is None and mario_a_amount < 10:
                print(f"Placing mario at {mario_spot}")
                agent.place_tower(TowerType.FIRE_MARIO,
                                  '2a', mario_spot)
                agent.send_chat('放置lv 2 mario')
                mario_a_amount += 1
                mario_spots.remove(mario_spot)
                # print(pos)
                break
    # check the number of flying enemies
    if now - flyers_last_check_time >= 6:
        flyers_last_check_time = now
        # get all flying enemies
        all_enemies = agent.get_all_enemies(True)
        flyers = [e for e in all_enemies if e.flying]
        num_flyers = len(flyers)
        if num_flyers > 3:
            # place mario for flyers
            place_mario_for_flyers(agent, terrain, fly_path)

    # luigi
    if now >= 120:
        for luigi_spot in luigi_spots:
            if agent.get_money(True) >= 2900 and agent.get_tower(True, luigi_spot) is None:
                print(f"Placing luigi at {luigi_spot}")
                agent.place_tower(TowerType.ICE_LUIGI,
                                  '3b', luigi_spot)
                agent.send_chat('放置lv 3 luigi')
                luigi_spots.remove(luigi_spot)
                # print(pos)
                break
    # luigi2
    if now >= 150:
        for luigi_spot in luigi2_spots:
            if agent.get_money(True) >= 2900 and agent.get_tower(True, luigi_spot) is None:
                print(f"Placing luigi at {luigi_spot}")
                agent.place_tower(TowerType.ICE_LUIGI,
                                  '3a', luigi_spot)
                agent.send_chat('放置lv 3a luigi')
                luigi2_spots.remove(luigi_spot)
                # print(pos)
                break

    # mario 2
    if now >= 100:
        for mario_spot in mario_spots:
            if agent.get_money(True) >= 1400 and agent.get_tower(True, mario_spot) is None and mario_a_amount < 10:
                print(f"Placing mario at {mario_spot}")
                agent.place_tower(TowerType.FIRE_MARIO,
                                  '2a', mario_spot)
                agent.send_chat('放置lv 2 mario')
                mario_a_amount += 1
                mario_spots.remove(mario_spot)
                # print(pos)
                break

    # this is upgrade
    to_delete = []
    towers = agent.get_all_towers(True)
    for tower in towers:
        # print(f'tower_level_a={tower.level_a}')
        # print(f'money={agent.get_money(True)}')
        if tower.level_a == 1 and agent.get_money(True) >= 1200:
            agent.place_tower(tower.type, '2a', tower.position)
            agent.send_chat('放置lv 2a')
            print('haha')
            to_delete.append(tower)
        elif tower.level_b == 1 and agent.get_money(True) >= 1200:
            agent.place_tower(tower.type, '2b', tower.position)
            agent.send_chat('放置lv 2b')
            to_delete.append(tower)
        elif tower.level_a == '2' and agent.get_money(True) >= 2800:
            agent.place_tower(tower.type, '3a', tower.position)
            agent.send_chat('放置lv 3a')
            print(tower)
            to_delete.append(tower)
        elif tower.level_b == '2' and agent.get_money(True) >= 2800:
            agent.place_tower(tower.type, '3b', tower.position)
            agent.send_chat('放置lv3b')
            to_delete.append(tower)
        # for tower in to_delete:
        #     towers.append(agent.get_tower(True, tower.position))
        #     towers.remove(tower)
        for tower in to_delete:
            updated = agent.get_tower(True, tower.position)
            if updated is not None:
                towers.append(updated)

            # Remove the one with matching position (even if it's a different object)
            towers = [t for t in towers if t.position != tower.position]

        break
    # extra
    nowMoney = agent.get_the_radiant_core_of_stellar_faith()
    if now >= 150 and nowMoney >= 2500:
        agent.disconnect()
        print('did')

    # 2. 分數、金錢、收入
print("Scores:", agent.get_scores(True),
      "(Me) /", agent.get_scores(False), "(Opp)")
print("Money: ", agent.get_money(True),
      "(Me) /", agent.get_money(False), "(Opp)")
print("Income:", agent.get_income(True), "(Me) /",
      agent.get_income(False), "(Opp)\n")
'''
# 3. 波次與時間
print("Wave:", agent.get_current_wave())
print("Remain time:", f"{agent.get_remain_time():.2f}s")
print("Until next wave:", f"{agent.get_time_until_next_wave():.2f}s\n")

# 4. 路徑
print("System path (ground):", [(c.x, c.y)
      for c in agent.get_system_path(False)])
print("Opponent path (air):",  [(c.x, c.y)
      for c in agent.get_opponent_path(True)], "\n")

# 5. 塔操作
pos = Vector2(5, 5)
if agent.get_tower(True, pos) is None:
    print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
    agent.place_tower(TowerType.FIRE_MARIO, "1", pos)
print("All my towers:", agent.get_all_towers(True))
# 設定塔的攻擊模式
agent.set_strategy(pos, TargetStrategy.CLOSE)

if agent.get_tower(True, Vector2(1, 2)) is None:
    agent.place_tower(TowerType.ICE_LUIGI, "1", pos)
time.sleep(3)
# 賣塔
agent.sell_tower(Vector2(1, 1))
print("After sell:", agent.get_all_towers(True), "\n")

# 6. 出兵
agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
print("Opp enemies:", agent.get_all_enemies(False))
print("KOOPA cooldown:",
      f"{agent.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA):.2f}s\n")

# 7. 法術
agent.cast_spell(SpellType.POISON, Vector2(3, 3))
print("My POISON CD:",
      f"{agent.get_spell_cooldown(True, SpellType.POISON):.2f}s\n")

# 8. 聊天
agent.set_name("OuO")
agent.set_chat_name_color("DCB5FF")
sent = agent.send_chat("OuO love you ! <3")
history = agent.get_chat_history(5)
for src, msg in history:
    if src == chatSource.PLAYER_SELF:
        who = "OuO"
    elif src == chatSource.PLAYER_OTHER:
        who = "Loser"
    else:
        who = "System"
    print(f"[{who}]", msg)
print()


while True:
    remain_time = agent.get_remain_time()

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

    # chat
    agent.send_chat('你說飛行敵人太強，其實是你太習慣凡事都想一步解決。')

    agent.send_chat('')

    agent.send_chat('')

    agent.send_chat('')

    agent.send_chat('')
'''
