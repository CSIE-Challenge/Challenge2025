import time
from time import sleep
from math import sqrt
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource, Tower

#連接登入種子
agent = GameClient(7749, "d3b9a23f")
time.sleep(5)

agent.set_name("贏政馭紅姊")
agent.ntu_student_id_card() 

if agent.get_the_radiant_core_of_stellar_faith > 2500 :
 agent.disconnect()
else:
 agent.boo()

# 取得整張地圖的地形資訊（2D 陣列）
terrain = agent.get_all_terrain()

empty_list = []  # 空地 (可放塔)
obstacle_list = []  # 障礙 (不能放塔)
road_list  = []  # 路徑 (敵人會走)

terrain_map = agent.get_all_terrain()  # 獲取整個地圖的地形資訊

#檢測每個座標的類型，並加入清單
for map_x in range(16):    
    for map_y in range(21): 
        terrain = terrain_map[map_x][map_y]

        if terrain == TerrainType.EMPTY:
            empty_list.append((map_x, map_y))
        elif terrain == TerrainType.ROAD:
            road_list.append((map_x, map_y))

print(f'空地{empty_list}')
print(f'道路{road_list}')

def count_covered_tiles(center, radius, path):
    count = 0
    for point in path:
        px = point.x
        py = point.y
        if (center[0] - px) ** 2 + (center[1] - py) ** 2 <= radius ** 2:
            count += 1
    return count

#定義塔的設定
ground_tower_type = TowerType.DONKEY_KONG
ground_tower_upgrade = "1"
ground_range = 2

air_tower_type = TowerType.SHY_GUY
air_tower_upgrade = "1"
air_range = 1   

luigi_tower_type = TowerType.ICE_LUIGI
luigi_tower_upgrade = '1'
luigi_range = 2

used_positions = set()

ground_scores = []
air_scores = []
luigi_scores = []

system_path = agent.get_system_path(False)
opponent_path = agent.get_opponent_path(False)

# 結合並去除重複點（轉成座標元組）
combined_ground_path = list({(p.x, p.y) for p in system_path + opponent_path})

# 轉換回 Vector2 格式
ground_path = [Vector2(x, y) for x, y in combined_ground_path]

system_air_path = agent.get_system_path(True)
opponent_air_path = agent.get_opponent_path(True)

combined_air_path = list({(p.x, p.y) for p in system_air_path + opponent_air_path})
air_path = [Vector2(x, y) for x, y in combined_air_path]

luigi_path = list({(p.x, p.y) for p in ground_path + air_path})
luigi_path = [Vector2(x, y) for x, y in luigi_path]

#根據覆蓋格數建立排序清單
for pos in empty_list:
    ground_score = count_covered_tiles(pos, ground_range, ground_path)
    air_score = count_covered_tiles(pos, air_range, air_path )
    luigi_score = count_covered_tiles(pos, luigi_range, luigi_path)

    if ground_score > 0:
        ground_scores.append((pos, ground_score))
    if air_score > 0:
        air_scores.append((pos, air_score))
    if luigi_score > 0:
        luigi_scores.append((pos, luigi_score))

# 排序：覆蓋越多越優先
ground_scores.sort(key=lambda x: x[1], reverse=True)
air_scores.sort(key=lambda x: x[1], reverse=True)
luigi_scores.sort(key=lambda x: x[1], reverse=True)

# 記錄目前嘗試到哪個位置
g_i = 0
a_i = 0
l_i = 0

place_ground_next = 0
placed_ground_count = 0  # 已放置的地面塔數量
placed_air_count = 0     # 已放置的空中塔數量
placed_luigi_count = 0   # 已放置的路易吉數量
placed_count = placed_air_count + placed_ground_count + placed_luigi_count
Tower_cost = 450

starting_point = agent.get_system_path(False)
start = starting_point[0]

while g_i < len(ground_scores) or a_i < len(air_scores) or l_i < len(luigi_score):

    while agent.get_game_status() != GameStatus.RUNNING:
     agent = GameClient(7749, "d3b9a23f")
     time.sleep(5)

    money = agent.get_money(True)
    remain_time = agent.get_remain_time()

    # 處理地面塔
    if place_ground_next == 0 and g_i < len(ground_scores):
        pos, score = ground_scores[g_i]
        if pos in used_positions:
            g_i += 1
        elif agent.get_money(True) >= Tower_cost :
            agent.place_tower(ground_tower_type, ground_tower_upgrade, Vector2(*pos))
            agent.set_strategy(pos,TargetStrategy.FIRST)
            used_positions.add(pos)
            placed_count += 1
            print(f"地面塔放在 {pos}，覆蓋地面格數：{score}")
            g_i += 1
            time.sleep(0.2)
            place_ground_next = 1

    # 處理空中塔
    if place_ground_next == 1 and a_i < len(air_scores):
        pos, score = air_scores[a_i]
        if pos in used_positions:
            a_i += 1
        elif agent.get_money(True) >= Tower_cost:
            agent.place_tower(air_tower_type, air_tower_upgrade, Vector2(*pos))
            agent.set_strategy(pos,TargetStrategy.FIRST)
            used_positions.add(pos)
            placed_count += 1
            print(f"空中塔放在 {pos}，覆蓋空中格數：{score}")
            a_i += 1
            time.sleep(0.2)
            place_ground_next = 2
        time.sleep(0.1)

        #處理路易吉
    if place_ground_next == 2 and l_i < len(luigi_scores) and placed_count >= 9:
        pos, score = luigi_scores[l_i]
        if pos in used_positions:
            l_i += 1
        elif agent.get_money(True) >= Tower_cost:
            agent.place_tower(luigi_tower_type, luigi_tower_upgrade, Vector2(*pos))
            agent.set_strategy(pos,TargetStrategy.FIRST)
            used_positions.add(pos)
            placed_count += 1
            print(f"路易吉塔放在 {pos}，覆蓋混合格數：{score}")
            l_i += 1
            time.sleep(0.2)
            place_ground_next = 0  # 回到地面塔

    elif place_ground_next == 2 and l_i < len(luigi_scores):
        place_ground_next = 0
        time.sleep(0.2)

    while placed_count == 10 :
        ground_tower_upgrade = "2a"
        air_tower_upgrade = "2b"
        luigi_tower_upgrade = '2b'
        used_positions = set()
        Tower_cost = 1350
        ground_range = 2
        air_range = 1
        luigi_range = 2
        break

    while placed_count == 20 :
        ground_tower_upgrade = "3a"
        air_tower_upgrade = "3b"
        luigi_tower_upgrade = '3b'
        used_positions = set()
        ground_range = 3
        air_range = 2
        luigi_range = 3
        Tower_cost = 2900
        break

poison_cd = agent.get_spell_cooldown(True, SpellType.POISON)
if poison_cd == 0:
    all_enemies = agent.get_all_enemies(True)
    poison_targets = [
        EnemyType.GOOMBA, EnemyType.BUZZY_BEETLE, 
        EnemyType.KOOPA, EnemyType.SPINY_SHELL
    ]
    for enemy in all_enemies:
        if enemy.type in poison_targets:
            agent.cast_spell(SpellType.POISON, enemy.position)
            print(f"使用毒藥在 {enemy.type.name} 的位置 {enemy.position}")

    if remain_time < 276:
        double_income_CD = agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME)
        if double_income_CD == 0:
            agent.cast_spell(SpellType.DOUBLE_INCOME) # 雙倍金錢
            print('使用雙倍金錢')

    teleport_cd = agent.get_spell_cooldown(True, SpellType.TELEPORT)
    all_enemies = agent.get_all_enemies(True)
    enemy_types = [e.type for e in all_enemies]

    income = agent.get_income(True)
    GO_CD = agent.get_unit_cooldown(EnemyType.GOOMBA) # 栗
    BU_CD = agent.get_unit_cooldown(EnemyType.BUZZY_BEETLE) # 藍龜
    KP_CD = agent.get_unit_cooldown(EnemyType.KOOPA_PARATROOPA) # 飛龜
    SP_CD = agent.get_unit_cooldown(EnemyType.SPINY_SHELL) # 綠龜
    if GO_CD == 0 and remain_time > 33 and remain_time < 285 :
        agent.spawn_unit(EnemyType.GOOMBA)
    elif money >= 1000 and KP_CD == 0 and remain_time > 85 and remain_time < 261:
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
        if money >= 1000 and BU_CD == 0:
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            if money >= 1000 and SP_CD == 0:
                agent.spawn_unit(EnemyType.SPINY_SHELL) # 放置單位

    if teleport_cd == 0:
        target_enemy = None

        # 設定傳送優先順序
        priority_list = [
            EnemyType.KOOPA_JR,
            EnemyType.KOOPA,
            EnemyType.WIGGLER,
            EnemyType.KOOPA_PARATROOPA,
            EnemyType.SPINY_SHELL
        ]

        for p_type in priority_list:
            # 搜尋第一個符合的敵人
            for enemy in all_enemies:
                if enemy.type == p_type:
                    target_enemy = enemy
                    break
            if target_enemy:
                break  # 找到後就不用檢查其他敵人

        if target_enemy:
            agent.cast_spell(SpellType.TELEPORT, target_enemy.position)
            print(f"對 {target_enemy.type.name} 使用傳送魔法，位置：{target_enemy.position}")

    agent.send_chat("大家好，我是秦始皇。  我今天是騎北極熊來的！  (默默開始唱歌) 「你撫琵琶奏琴弦；我坐戲子樓台前」")