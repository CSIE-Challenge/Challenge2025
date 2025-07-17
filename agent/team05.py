# Copyright © 2025 mtmatt, ouo. All rights reserved.

import time
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

agent = GameClient(7749, "b558a928")  # Replace with your token

print("Waiting for game to RUNNING...")
while agent.get_game_status() != GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

agent.set_name("boo boo五超讚")

agent.set_the_radiant_core_of_stellar_faith(3938)
agent.disconnect()
while True:
    
    if agent.get_money(False) >= 460:
        agent.boo()
    
    #嗆
    agent.send_chat('菜狗')
    ememies = agent.get_all_enemies(True)
    for i in ememies :
        if i.type == EnemyType.BUZZY_BEETLE :
            agent.cast_spell(SpellType.TELEPORT, i.position )

    #攻擊
    if agent.get_remain_time() <= 300 and agent.get_remain_time() >= 35:
        agent.spawn_unit(EnemyType.GOOMBA)
    if int(agent.get_remain_time() % 4) == 0 and agent.get_remain_time() <= 232:
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
    if agent.get_remain_time() <= 40 :
            agent.spawn_unit(EnemyType.KOOPA_JR)
            
    #雙倍錢
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    
    #傳送門
    if agent.get_remain_time() < 270:
        agent.cast_spell(SpellType.TELEPORT, Vector2(0, 0))
    
    terrain = agent.get_all_terrain()
    towers = agent.get_all_towers(True)
    
    #印時間
    print(agent.get_remain_time())
    
    #毒藥
    print(agent.get_spell_cooldown(True, SpellType.POISON))
    if agent.get_spell_cooldown(True, SpellType.POISON) == 0:
        for c in agent.get_system_path(False):
            if agent.get_remain_time() < 300 :
                if agent.get_spell_cooldown(True, SpellType.POISON) != 0:
                    pass
                else:
                    agent.cast_spell(SpellType.POISON, Vector2(c.x, c.y))
    
    #很多馬力歐(剩3:20前放)
    if agent.get_remain_time() > 220 :
        for (row, data) in enumerate(terrain):
            for (col, tile) in enumerate(data):
                pos = (row, col)
                if tile == TerrainType.EMPTY :
                    cnt = 0
                    if terrain[row+1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row-1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col+1] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col-1] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if cnt == 1 :
                        agent.place_tower(TowerType.FIRE_MARIO, '1', Vector2(row, col))      
        for c in agent.get_system_path(True):
            for (row, data) in enumerate(terrain):
                for (col, tile) in enumerate(data):
                    if c == tile :
                        agent.place_tower(TowerType.FIRE_MARIO, '1',Vector2(row, col)) 
         
    
    #賣馬力歐
    elif agent.get_remain_time() > 218 :
        for (row, data) in enumerate(terrain):
            for (col, tile) in enumerate(data):
                pos = (row, col)
                agent.sell_tower(Vector2(row, col))
        

                    
    #馬力歐2a(2:30)
    elif agent.get_remain_time() > 150:
        for (row, data) in enumerate(terrain):
            for (col, tile) in enumerate(data):
                pos = (row, col)
                if tile == TerrainType.EMPTY :
                    cnt = 0
                    if terrain[row+1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row-1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col+1] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col-1] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if cnt == 1 :
                        agent.place_tower(TowerType.FIRE_MARIO, '2a', Vector2(row, col))
        for c in agent.get_system_path(True):
            for (row, data) in enumerate(terrain):
                for (col, tile) in enumerate(data):
                    if c == tile :
                        agent.place_tower(TowerType.FIRE_MARIO, '2a',Vector2(row, col)) 
        agent.spawn_unit(EnemyType.GOOMBA)   
    #黑喝(1:40)
    elif agent.get_remain_time() > 100:
        for (row, data) in enumerate(terrain):
            for (col, tile) in enumerate(data):
                pos = (row, col)
                if tile == TerrainType.EMPTY :
                    cnt = 0
                    if terrain[row+1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row-1][col] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col+1] == TerrainType.ROAD:
                        cnt = cnt + 1
                    if terrain[row][col-1] == TerrainType.ROAD:
                        cnt = cnt + 1   
                    if cnt >= 2:        
                        agent.place_tower(TowerType.SHY_GUY, '2b', Vector2(row, col)) 
        for c in agent.get_system_path(True):
            for (row, data) in enumerate(terrain):
                for (col, tile) in enumerate(data):
                    if c == tile :
                        agent.place_tower(TowerType.SHY_GUY, '2b',Vector2(row, col))
                  
                         
    #馬力歐3a  
    elif agent.get_remain_time() > 0:
        for (row, data) in enumerate(terrain):
            for (col, tile) in enumerate(data):
                pos = (row, col)
                agent.place_tower(TowerType.FIRE_MARIO, '3a', Vector2(row, col)) 