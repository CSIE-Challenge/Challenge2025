
import time
import random
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

agent = GameClient(7749, "ac5619b1")  # Replace with your token

terrain = agent.get_all_terrain()

one_side = []
two_or_above_side = []
no_side = []

agent.ntu_student_id_card()
#把東西全部打九折 但不知道有沒有用


for i in range (14):
    for j in range(19):
        side = 0 
        if terrain[i][j+1] == TerrainType.ROAD:
            side += 1
        if terrain[i+2][j+1] == TerrainType.ROAD:
            side += 1
        if terrain[i+1][j] == TerrainType.ROAD:
            side += 1
        if terrain[i+1][j+2] == TerrainType.ROAD:
            side += 1
        if side == 0 :
            no_side.append((i+1,j+1))
        elif side == 1 :
            one_side.append((i+1,j+1))
        else:
            two_or_above_side.append((i+1,j+1))
        
print(one_side)


        

while True:
    #wave 1: 狂出力寶寶 放全部咒語
    x2money_cooldown = agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME)
    poison_cooldown = agent.get_spell_cooldown(True,SpellType.POISON)
    teleport_cooldown = agent.get_spell_cooldown(True,SpellType.TELEPORT)
    enemy_information = agent.get_all_enemies(True)
    if x2money_cooldown == 0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    elif poison_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.GOOMBA or enemy.type == EnemyType.BUZZY_BEETLE or enemy.type == EnemyType.WIGGLER or enemy.type == EnemyType.SPINY_SHELL:
                agent.cast_spell(SpellType.POISON,enemy.position)
    elif teleport_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.KOOPA or enemy.type == EnemyType.KOOPA_JR:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
            elif enemy.type == EnemyType.WIGGLER:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
    #
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    agent.spawn_unit(EnemyType.GOOMBA)
    wave = agent.get_current_wave()

    if wave >= 2:
        break
for i in range(5):
    agent.place_tower(TowerType.FIRE_MARIO, "1" ,  Vector2(9,i+8))
    agent.place_tower(TowerType.FIRE_MARIO, "1" ,  Vector2(8,i+8))
heho = 0
while True:
    x2money_cooldown = agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME)
    poison_cooldown = agent.get_spell_cooldown(True,SpellType.POISON)
    teleport_cooldown = agent.get_spell_cooldown(True,SpellType.TELEPORT)
    enemy_information = agent.get_all_enemies(True)
    if x2money_cooldown == 0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    elif poison_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.GOOMBA or enemy.type == EnemyType.BUZZY_BEETLE or enemy.type == EnemyType.WIGGLER or enemy.type == EnemyType.SPINY_SHELL:
                agent.cast_spell(SpellType.POISON,enemy.position)
    elif teleport_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.KOOPA or enemy.type == EnemyType.KOOPA_JR:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
            elif enemy.type == EnemyType.WIGGLER:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
    wave = agent.get_current_wave()
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    agent.spawn_unit(EnemyType.GOOMBA)
    money = agent.get_money(True)
    if money >= 1200 and heho%2 == 0:
        place = random.randint(0,len(one_side)-1)
        place_vec = one_side[place]
        heho_pos = random.randint(0,len(one_side)-1)
        tw = agent.get_tower(True,Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
        while  tw == TowerType.ICE_LUIGI or tw == TowerType.DONKEY_KONG or tw == TowerType.FORT or tw ==TowerType.SHY_GUY :
            heho_pos = random.randint(0,len(one_side)-1)
            #debug log
            tw = agent.get_tower(True,Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
        agent.place_tower(TowerType.SHY_GUY, "2b" ,  Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
        heho+=1
        sell0 = one_side[heho_pos][0]
        sell1 = one_side[heho_pos][1]
    elif money >= 1600 and heho%2 == 1 :
        agent.sell_tower(Vector2(sell0,sell1))
        agent.place_tower(TowerType.SHY_GUY, "3b" ,  Vector2(sell0,sell1))
        heho+=1
    if wave >= 7 :
        break
order = 0
while True :
    #Challenge-OuO
    if agent.get_remain_time() <= 10 and agent.get_the_radiant_core_of_stellar_faith() > 180:
        agent.spam("掐潤吉好帥", 72, 	"#00FFFF")
    x2money_cooldown = agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME)
    poison_cooldown = agent.get_spell_cooldown(True,SpellType.POISON)
    teleport_cooldown = agent.get_spell_cooldown(True,SpellType.TELEPORT)
    enemy_information = agent.get_all_enemies(True)
    if x2money_cooldown == 0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)
    elif poison_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.GOOMBA or enemy.type == EnemyType.BUZZY_BEETLE or enemy.type == EnemyType.WIGGLER or enemy.type == EnemyType.SPINY_SHELL:
                agent.cast_spell(SpellType.POISON,enemy.position)
    elif teleport_cooldown == 0:
        for enemy in enemy_information:
            if enemy.type == EnemyType.KOOPA or enemy.type == EnemyType.KOOPA_JR:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
            elif enemy.type == EnemyType.WIGGLER:
                agent.cast_spell(SpellType.TELEPORT,enemy.position)
    wave = agent.get_current_wave()
    agent.cast_spell(SpellType.DOUBLE_INCOME)
    agent.spawn_unit(EnemyType.GOOMBA)
    agent.spawn_unit(EnemyType.KOOPA_JR)
    agent.spawn_unit(EnemyType.KOOPA)
    print(order)
    print(heho)
    if order%2 == 0:
        if money >= 1200 and heho%2 == 0:
            place = random.randint(0,len(one_side)-1)
            place_vec = one_side[place]
            heho_pos = random.randint(0,len(one_side)-1)
            tw = agent.get_tower(True,Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
            while  tw == TowerType.ICE_LUIGI or tw == TowerType.DONKEY_KONG or tw == TowerType.FORT or tw ==TowerType.SHY_GUY :
                heho_pos = random.randint(0,len(one_side)-1)
                #debug log
                tw = agent.get_tower(True,Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
            agent.place_tower(TowerType.SHY_GUY, "2b" ,  Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
            print("placed shyguy")
            heho+=1
            sell0 = one_side[heho_pos][0]
            sell1 = one_side[heho_pos][1]
            order +=1
        elif money >= 1600 and heho%2 == 1 :
            agent.sell_tower(Vector2(sell0,sell1))
            agent.place_tower(TowerType.SHY_GUY, "3b" ,  Vector2(sell0,sell1))
            print("upgrade shyguy")
            heho+=1
            order+=1
    elif order % 6 == 1 or order % 6 == 5:
        if money >= 1200 :
            place = random.randint(0,len(two_or_above_side)-1)
            place_vec = two_or_above_side[place]
            luigi_pos = random.randint(0,len(two_or_above_side)-1)
            tw = agent.get_tower(True,Vector2(one_side[heho_pos][0],one_side[heho_pos][1]))
            while  tw == TowerType.ICE_LUIGI or tw == TowerType.DONKEY_KONG or tw == TowerType.FORT or tw ==TowerType.SHY_GUY :
                luigi_pos = random.randint(0,len(two_or_above_side)-1)
                #debug log
                tw = agent.get_tower(True,Vector2(two_or_above_side[luigi_pos][0],two_or_above_side[luigi_pos][1]))
            agent.place_tower(TowerType.ICE_LUIGI, "2b" ,  Vector2(two_or_above_side[luigi_pos][0],two_or_above_side[luigi_pos][1]))
            print("luigi")
            order +=1
    elif order %6 == 3 :
        if money >= 2800 :
            place = random.randint(0,len(two_or_above_side)-1)
            place_vec = two_or_above_side[place]
            gorilla_pos = random.randint(0,len(two_or_above_side)-1)
            tw = agent.get_tower(True,Vector2(two_or_above_side[gorilla_pos][0],two_or_above_side[gorilla_pos][1]))
            while  tw == TowerType.ICE_LUIGI or tw == TowerType.DONKEY_KONG or tw == TowerType.FORT or tw ==TowerType.SHY_GUY :
                gorilla_pos = random.randint(0,len(two_or_above_side)-1)
                #debug log
                tw = agent.get_tower(True,Vector2(two_or_above_side[gorilla_pos][0],two_or_above_side[gorilla_pos][1]))
            agent.place_tower(TowerType.DONKEY_KONG, "3a" ,  Vector2(two_or_above_side[gorilla_pos][0],two_or_above_side[gorilla_pos][1]))
            print("DK")
            order +=1

    
#目前剩餘問題:到後期 order選到同一格的時候會卡死，導致沒辦法放塔。
#最後會剩一堆錢，希望能把所有塔升到三階並盡量填滿格子
#然後剩下的克金點可以隨機幫我們發召部好帥的彈幕謝謝
#謝謝challenge組


