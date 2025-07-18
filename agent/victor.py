
import time, copy, random, math
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource


agent = GameClient(7749, "ffffffff")  # Replace with your token
agent.set_name("victor0206")
print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

SYSTEM_RATIO = 1
PLAYER_RATIO = 0.7
GROUND_RATIO = 1
AIR_RATIO = 0.5
LEVEL_MAP = {
    (1, 1): "1",
    (2, 1): "2a",
    (1, 2): "2b",
    (3, 1): "3a",
    (1, 3): "3b",
}

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
        # print(pos, ":", count_road, count1, count2)
        if road < count_road:
            road, ground_count, air_count = count_road, count1, count2
        dx, dy = -dy, dx
    if 500 * (1 - 1 / 2 ** ground_count) > 20 * (ground_count + air_count):
        return (500 * (1 - 1 / 2 ** ground_count), "2a")
    return (20 * (ground_count + air_count) / 2, "2b")

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
    return (ground_count + air_count * 10)

best, ord = {}, []

def best_tower():
    for (row, data) in enumerate(terrain):
        for (col, tile) in enumerate(data):
            if tile == TerrainType.EMPTY:
                val, tp = fort_count(Vector2(row, col))
                if val < 495:
                    ival = ice_count(Vector2(row, col))
                    tp = random.choice([TowerType.ICE_LUIGI, TowerType.FIRE_MARIO])
                    # if ival > 3.5:
                    #     best[(row, col)] = (TowerType.ICE_LUIGI, "2b")
                    #     ord.append((TowerType.ICE_LUIGI, "2b", ival, (row, col), 1200))
                    if ival > 0:
                        best[(row, col)] = (tp, "1")
                        ord.append((tp, "1", ival, (row, col), 400))
                        ord.append((tp, "2a", ival / 1.15, (row, col), 800))
                        ord.append((tp, "3a", ival / 1.3, (row, col), 1600))

                else:
                    best[(row, col)] = (TowerType.FORT, tp)
                    ord.append((TowerType.FORT, tp, val, (row, col), 1200))
                    ord.append((TowerType.FORT, "3" + tp[1], val - 2, (row, col), 1600))

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

ord.sort(key=lambda x: (x[2]))
ord.reverse()
print(ord)

possible = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4]
next, ok = 4, 0

while True:
    remain_time = agent.get_remain_time()
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    
    all_enemies = agent.get_all_enemies(True)
    if agent.get_spell_cooldown(True, SpellType.POISON) == 0:
        cells = {}
        for enemy in all_enemies:
            if (enemy.position.x, enemy.position.y) not in cells:
                cells[(enemy.position.x, enemy.position.y)] = 0
            cells[(enemy.position.x, enemy.position.y)] += 1
        if len(cells) > 0:
            cell_with_most_enemies = max(cells, key=cells.get)
            if cells[cell_with_most_enemies] > 2:
                agent.cast_spell(SpellType.POISON, Vector2(cell_with_most_enemies[0], cell_with_most_enemies[1]))
    
    if agent.get_spell_cooldown(True, SpellType.TELEPORT) == 0:
        cells = {}
        for enemy in all_enemies:
            if (enemy.position.x, enemy.position.y) not in cells:
                cells[(enemy.position.x, enemy.position.y)] = 0
            cells[(enemy.position.x, enemy.position.y)] += enemy.damage
        if len(cells) > 0:
            cell_with_most_enemies = max(cells, key=cells.get)
            if cells[cell_with_most_enemies] > 6000:
                agent.cast_spell(SpellType.TELEPORT, Vector2(cell_with_most_enemies[0], cell_with_most_enemies[1]))


    my_towers, nums, towers_map, my_money, remain_time = agent.get_all_towers(True), [0, 0, 0, 0, 0, 0], {}, agent.get_money(True), agent.get_remain_time()
    for tower in my_towers:
        nums[tower.type] += 1
        towers_map[(tower.position.x, tower.position.y)] = tower
    if remain_time > 30:
        if agent.get_income(True) < 300:
            agent.spawn_unit(EnemyType.GOOMBA)
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        elif len(my_towers) > 13 and agent.get_income(True) < 550:
            agent.spawn_unit(EnemyType.GOOMBA)
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            agent.spawn_unit(EnemyType.SPINY_SHELL)
        elif len(my_towers) > 18 and agent.get_income(True) < 750:
            agent.spawn_unit(EnemyType.GOOMBA)
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
            agent.spawn_unit(EnemyType.KOOPA_JR)
            agent.spawn_unit(EnemyType.WIGGLER)
        elif len(my_towers) > 25 and agent.get_income(True) < 1000:
            agent.spawn_unit(EnemyType.KOOPA_JR)
            agent.spawn_unit(EnemyType.WIGGLER)
            agent.spawn_unit(EnemyType.KOOPA)
        elif len(my_towers) > 40:
            agent.spawn_unit(EnemyType.KOOPA_JR)
            agent.spawn_unit(EnemyType.WIGGLER)
            agent.spawn_unit(EnemyType.KOOPA)

    my_money = agent.get_money(True)
    # print("next:", next, "ok:", ok, "my_money:", my_money, "remain_time:", remain_time)
    for (tower_type, tower_level, val, pos, tower_cost) in ord:
        tower = towers_map[(pos[0], pos[1])] if (pos[0], pos[1]) in towers_map else None
        if (tower is None or LEVEL_MAP[(tower.level_a, tower.level_b)] < tower_level) and tower_type == next:
            if my_money >= tower_cost:
                # print(f"Placing tower {tower_type} at {pos} with level {tower_level} (cost: {tower_cost})")
                agent.place_tower(tower_type, tower_level, Vector2(*pos))
                next, ok = random.choice(possible), 0
            else:
                ok = 1
            break

    # print("after next:", next, "ok:", ok, "my_money:", my_money, "remain_time:", remain_time)
    if ok == 0:
        next = random.choice(possible)
            # if agent.get_money(True) >= tower_cost:
            #     agent.place_tower(tower_type, tower_level, Vector2(*pos))
            # else:
            #     break
