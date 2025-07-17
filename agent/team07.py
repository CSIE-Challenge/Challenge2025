import api
import random
import time

agent = api.GameClient(7749, '511a6fbe')

print("Waiting for game to RUNNING...")
while agent.get_game_status() != api.GameStatus.RUNNING:
    time.sleep(0.5)
print("Game RUNNING!\n")

agent.set_name("chipichipichapachapadubidubidabadaba")
agent.set_chat_name_color("DCB5FF")
def type1_settings(terrain):
    #one-time setting
        #map recognition
    global map_number
    map_number=-1
    if terrain[2][0]==api.TerrainType.OBSTACLE and terrain[2][1]==api.TerrainType.EMPTY and terrain[2][2]==api.TerrainType.EMPTY and terrain[2][3]==api.TerrainType.OBSTACLE and terrain[2][4]==api.TerrainType.OBSTACLE and terrain[2][5]==api.TerrainType.OBSTACLE:
        map_number = 1
    elif terrain[2][0]==api.TerrainType.OBSTACLE and terrain[2][1]==api.TerrainType.EMPTY and terrain[2][2]==api.TerrainType.EMPTY and terrain[2][3]==api.TerrainType.ROAD and terrain[2][4]==api.TerrainType.EMPTY and terrain[2][5]==api.TerrainType.EMPTY:
        map_number = 2
    elif terrain[2][0]==api.TerrainType.OBSTACLE and terrain[2][1]==api.TerrainType.OBSTACLE and terrain[2][2]==api.TerrainType.OBSTACLE and terrain[2][3]==api.TerrainType.EMPTY and terrain[2][4]==api.TerrainType.EMPTY and terrain[2][5]==api.TerrainType.EMPTY:
        map_number = 3
    elif terrain[2][0]==api.TerrainType.OBSTACLE and terrain[2][1]==api.TerrainType.OBSTACLE and terrain[2][2]==api.TerrainType.ROAD and terrain[2][3]==api.TerrainType.ROAD and terrain[2][4]==api.TerrainType.ROAD and terrain[2][5]==api.TerrainType.OBSTACLE:
        map_number = 4
    elif terrain[2][0]==api.TerrainType.OBSTACLE and terrain[2][1]==api.TerrainType.OBSTACLE and terrain[2][2]==api.TerrainType.ROAD and terrain[2][3]==api.TerrainType.EMPTY and terrain[2][4]==api.TerrainType.EMPTY and terrain[2][5]==api.TerrainType.EMPTY:
        map_number = 6
    else:
        map_number = 5
    #============
    '''map_number=5'''
    #============
    '''if agent.get_terrain(Vector2(1,1)) == api.TerrainType.ROAD:'''
    #one time var setting
    global fort_placed_check,one_time_check_1,fort_upgraded_check, donkey_placed_check, fire_mario_placed_check, donkey_upgraded_check, fire_mario_upgraded_check
    global tower_status,random_map_tower_list_coord,random_map_tower_list_type
    global random_map_sec_1_tower_counter,disconect_used_times
    try:
        agent.ntu_student_id_card()
        print("discount_completed")
    except:
        pass
    random_map_sec_1_tower_counter=0
    fort_placed_check=[]
    donkey_placed_check = []
    fire_mario_placed_check = []
    fort_upgraded_check=[]
    donkey_upgraded_check = []
    fire_mario_upgraded_check = []
    random_map_tower_list_coord=[]
    random_map_tower_list_type=[]
    one_time_check_1=False
    disconect_used_times=0
    tower_status= [[False for _ in range(21)] for _ in range(16)]# to prevent section 2 mario overwrite section 1 tower
def type2_settings():
    #needs to update continuously
    try:
        agent.set_the_radiant_core_of_stellar_faith(90000)
    except:
        pass
    print(f"stellar={agent.get_the_radiant_core_of_stellar_faith}")
    global remain_time,our_scores,opponent_scores,our_money,opponent_money
    global our_income,opponent_income,general_terrain,current_wave
    global next_wave_counter,air_opponent_unit_path
    global land_system_unit_path,land_opponent_unit_path,air_system_unit_path
    global current_our_side_enemies,current_opponent_side_enemies
    global current_our_side_towers,current_opponent_side_towers
    remain_time = agent.get_remain_time()
    our_scores = agent.get_scores(True)
    opponent_scores = agent.get_scores(False)
    our_money = agent.get_money(True)
    opponent_money = agent.get_money(False)
    our_income = agent.get_income(True)
    opponent_income = agent.get_income(False)
    general_terrain=agent.get_all_terrain()
    current_wave=agent.get_current_wave()
    next_wave_counter=agent.get_time_until_next_wave()
    land_system_unit_path=agent.get_system_path(False)
    land_opponent_unit_path=agent.get_opponent_path(False)
    air_system_unit_path=agent.get_system_path(True)
    air_opponent_unit_path=agent.get_opponent_path(True)
    current_our_side_enemies=agent.get_all_enemies(True)
    current_opponent_side_enemies=agent.get_all_enemies(False)
    current_our_side_towers=agent.get_all_towers(True)
    current_opponent_side_towers=agent.get_all_towers(False)
def place_defense():
    global random_map_sec_1_tower_counter
    global random_map_tower_list_coord,random_map_tower_list_type
    type2_settings()
    if map_number==1:
        if len(fort_placed_check)==0:
            #first time in this function,need initialization
            for i in range(6):
                fort_placed_check.append(False)

        if len(donkey_placed_check)==0:
            #first time in this function,need initialization
            for i in range(8):
                donkey_placed_check.append(False)

        if False in fort_placed_check or False in donkey_placed_check:
            #section 1: placing 6 Lv1 forts + 8 Lv1 Donkey Kongs as fast as possible
            for i in range(6):
                if not fort_placed_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(1,i)
                        agent.place_tower(api.TowerType.FORT, '1', api.Vector2(coordination[0], coordination[1]))
                        fort_placed_check[i]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(fort_placed_check)'''
            for i in range(6, 14):
                if not donkey_placed_check[i-6]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(1,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                        donkey_placed_check[i-6]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(donkey_placed_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            '''print("測試1")'''
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==2:
        if len(fort_placed_check)==0:
            #first time in this function,need initialization
            for i in range(4):
                fort_placed_check.append(False)

        if len(donkey_placed_check)==0:
            #first time in this function,need initialization
            for i in range(7):
                donkey_placed_check.append(False)
        if len(fire_mario_placed_check)==0:
            #first time in this function,need initialization
            for i in range(4):
                fire_mario_placed_check.append(False)

        if False in fort_placed_check or False in donkey_placed_check or False in fire_mario_placed_check:
            #section 1: placing 4 Lv1 forts + 7 Lv1 Donkey Kongs + 4 Lv1 Fire Marios as fast as possible
            for i in range(7):
                if not donkey_placed_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                        donkey_placed_check[i]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(donkey_kong_placed_check)'''
            for i in range(7, 11):
                if not fire_mario_placed_check[i-7]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.FIRE_MARIO, '1', api.Vector2(coordination[0], coordination[1]))
                        fire_mario_placed_check[i-7]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(fire_mario_placed_check)'''
            for i in range(11, 15):
                if not fort_placed_check[i-11]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.FORT, '1', api.Vector2(coordination[0], coordination[1]))
                        fort_placed_check[i-11]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(fort_placed_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==3:
        if len(fort_placed_check)==0:
            #first time in this function,need initialization
            for i in range(6):
                fort_placed_check.append(False)

        if len(donkey_placed_check)==0:
            #first time in this function,need initialization
            for i in range(9):
                donkey_placed_check.append(False)

        if False in fort_placed_check or False in donkey_placed_check:
            #section 1: placing 6 Lv1 forts + 9 Lv1 Donkey Kongs as fast as possible
            for i in range(6):
                if not fort_placed_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(3,i)
                        agent.place_tower(api.TowerType.FORT, '1', api.Vector2(coordination[0], coordination[1]))
                        fort_placed_check[i]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(donkey_kong_placed_check)'''
            for i in range(6, 15):
                if not donkey_placed_check[i-6]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(3,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                        donkey_placed_check[i-6]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(fire_mario_placed_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==4:
        if len(donkey_placed_check)==0:
            #first time in this function,need initialization
            for i in range(11):
                donkey_placed_check.append(False)

        if False in donkey_placed_check:
            #section 1: placing 11 Lv1 Donkey Kongs as fast as possible
            for i in range(11):
                if not donkey_placed_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(4,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                        donkey_placed_check[i]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(donkey_kong_placed_check)'''
        else:
            # donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==6:
        if len(fort_placed_check)==0:
            #first time in this function,need initialization
            for i in range(7):
                fort_placed_check.append(False)

        if len(donkey_placed_check)==0:
            #first time in this function,need initialization
            for i in range(8):
                donkey_placed_check.append(False)

        if False in fort_placed_check or False in donkey_placed_check:
            #section 1: placing 6 Lv1 forts + 9 Lv1 Donkey Kongs as fast as possible
            for i in range(7):
                if not fort_placed_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(8,i)
                        agent.place_tower(api.TowerType.FORT, '1', api.Vector2(coordination[0], coordination[1]))
                        fort_placed_check[i]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(fort_placed_check)'''
            for i in range(7, 15):
                if not donkey_placed_check[i-7]:
                    #not placed yet
                    type2_settings()
                    if our_money>=400:
                        coordination=get_coordination(8,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                        donkey_placed_check[i-7]=True
                        tower_status[coordination[0]][coordination[1]]=True
                        type2_settings()
                        '''print(donkey_placed_check)'''
        else:
            print("placed_test")
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number == 5:
        type2_settings()
        if our_money>=400:
            if random_map_sec_1_tower_counter<=6:
                coordination=get_coordination(6,0)
                agent.place_tower(api.TowerType.DONKEY_KONG, '1', api.Vector2(coordination[0], coordination[1]))
                tower_status[coordination[0]][coordination[1]]=True
                random_map_sec_1_tower_counter+=1
                print(random_map_sec_1_tower_counter)
                random_map_tower_list_coord.append([coordination[0],coordination[1]])
                random_map_tower_list_type.append(api.TowerType.DONKEY_KONG)
            elif random_map_sec_1_tower_counter<=14:
                print("dev3")
                coordination=get_coordination(7,0)
                agent.place_tower(api.TowerType.FORT, '1', api.Vector2(coordination[0], coordination[1]))
                tower_status[coordination[0]][coordination[1]]=True
                random_map_sec_1_tower_counter+=1
                print(random_map_sec_1_tower_counter)
                random_map_tower_list_coord.append([coordination[0],coordination[1]])
                random_map_tower_list_type.append(api.TowerType.FORT)
            else:
                if current_section==1:
                    cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                    if cooldown==0 and our_money>=250:
                        agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                        type2_settings()
    #想法: 隨機或是有改動的時候，使用判斷，如果一個格子的terrain type = empty，而且上下左右其中一邊要有4個road(猜測用兩個flag)，才放我不知道你要放哪一個
def upgrade_defense():
    type2_settings()
    if map_number==1:
        if len(fort_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(6):
                fort_upgraded_check.append(False)

        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(8):
                donkey_upgraded_check.append(False)

        if False in fort_upgraded_check or False in donkey_upgraded_check:
            #section 1: placing 6 Lv1 forts + 8 Lv1 Donkey Kongs as fast as possible
            for i in range(6):
                if not fort_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(1,i)
                        agent.place_tower(api.TowerType.FORT, '2b', api.Vector2(coordination[0], coordination[1]))
                        fort_upgraded_check[i]=True
                        type2_settings()
                        '''print(fort_upgraded_check)'''
            for i in range(6, 14):
                if not donkey_upgraded_check[i-6]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(1,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i-6]=True
                        type2_settings()
                        '''print(donkey_upgraded_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==2:
        if len(fort_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(4):
                fort_upgraded_check.append(False)

        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(7):
                donkey_upgraded_check.append(False)
        if len(fire_mario_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(4):
                fire_mario_upgraded_check.append(False)

        if False in fort_upgraded_check or False in donkey_upgraded_check or False in fire_mario_upgraded_check:
            #section 1: placing 4 Lv1 forts + 7 Lv1 Donkey Kongs + 4 Lv1 Fire Marios as fast as possible
            for i in range(7):
                if not donkey_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i]=True
                        type2_settings()
                        '''print(donkey_kong_upgraded_check)'''
            for i in range(7, 11):
                if not fire_mario_upgraded_check[i-7]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.FIRE_MARIO, '2a', api.Vector2(coordination[0], coordination[1]))
                        fire_mario_upgraded_check[i-7]=True
                        type2_settings()
                        ''''print(fire_mario_upgraded_check)'''
            for i in range(11, 15):
                if not fort_upgraded_check[i-11]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(2,i)
                        agent.place_tower(api.TowerType.FORT, '2b', api.Vector2(coordination[0], coordination[1]))
                        fort_upgraded_check[i-11]=True
                        type2_settings()
                        '''print(fort_upgraded_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==3:
        if len(fort_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(6):
                fort_upgraded_check.append(False)

        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(9):
                donkey_upgraded_check.append(False)

        if False in fort_upgraded_check or False in donkey_upgraded_check:
            #section 1: placing 4 Lv1 forts + 7 Lv1 Donkey Kongs + 4 Lv1 Fire Marios as fast as possible
            for i in range(6):
                if not fort_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(3,i)
                        agent.place_tower(api.TowerType.FORT, '2b', api.Vector2(coordination[0], coordination[1]))
                        fort_upgraded_check[i]=True
                        type2_settings()
                        '''print(donkey_kong_upgraded_check)'''
            for i in range(6, 15):
                if not donkey_upgraded_check[i-6]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(3,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i-6]=True
                        type2_settings()
                        '''print(fire_mario_upgraded_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==4:
        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(11):
                donkey_upgraded_check.append(False)

        if False in donkey_upgraded_check:
            #section 1: placing 11 Lv1 Donkey Kongs as fast as possible
            for i in range(11):
                if not donkey_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(4,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i]=True
                        type2_settings()
                        '''print(donkey_kong_upgraded_check)'''
        else:
            # donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number==6:
        if len(fort_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(7):
                fort_upgraded_check.append(False)

        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(8):
                donkey_upgraded_check.append(False)

        if False in fort_upgraded_check or False in donkey_upgraded_check:
            #section 1: placing 4 Lv1 forts + 7 Lv1 Donkey Kongs + 4 Lv1 Fire Marios as fast as possible
            for i in range(7):
                if not fort_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(8,i)
                        agent.place_tower(api.TowerType.FORT, '2b', api.Vector2(coordination[0], coordination[1]))
                        fort_upgraded_check[i]=True
                        type2_settings()
                        '''print(donkey_kong_upgraded_check)'''
            for i in range(7, 15):
                if not donkey_upgraded_check[i-7]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=get_coordination(8,i)
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i-7]=True
                        type2_settings()
                        '''print(fire_mario_upgraded_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    elif map_number == 5:
        if len(fort_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(7):
                fort_upgraded_check.append(False)

        if len(donkey_upgraded_check)==0:
            #first time in this function,need initialization
            for i in range(8):
                donkey_upgraded_check.append(False)

        if False in fort_upgraded_check or False in donkey_upgraded_check:
            #section 1: placing 4 Lv1 forts + 7 Lv1 Donkey Kongs + 4 Lv1 Fire Marios as fast as possible
            for i in range(7):
                if not fort_upgraded_check[i]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=random_map_tower_list_coord[i]
                        agent.place_tower(api.TowerType.DONKEY_KONG, '2a', api.Vector2(coordination[0], coordination[1]))
                        fort_upgraded_check[i]=True
                        type2_settings()
                        '''print(donkey_kong_upgraded_check)'''
            for i in range(7, 15):
                if not donkey_upgraded_check[i-7]:
                    #not placed yet
                    type2_settings()
                    if our_money>=1200:
                        coordination=random_map_tower_list_coord[i-7]
                        agent.place_tower(api.TowerType.FORT, '2b', api.Vector2(coordination[0], coordination[1]))
                        donkey_upgraded_check[i-7]=True
                        type2_settings()
                        '''print(fire_mario_upgraded_check)'''
        else:
            # fort_placed_check以及donkey_placed_check都是True Chatgpt寫得但我不知道怎麼放到遊戲上執行
            if current_section==1:
                cooldown = agent.get_unit_cooldown(api.EnemyType.KOOPA_PARATROOPA)
                if cooldown==0 and our_money>=250:
                    agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
                    type2_settings()
    #想法: 隨機或是有改動的時候，使用判斷，如果一個格子的terrain type = empty，而且上下左右其中一邊要有4個road(猜測用兩個flag)，才放我不知道你要放哪一個
def get_coordination(type,i):
    #type list:
    #1~4:map (N) tower placing or upgrading for specific map
    #5:get random road-side coordination
    #6:get random road-corner coordination
    #7:get random 4-block-road side coordination
    type2_settings()
    if type==1:
        #map 1 fort initial placing
        coordination_list=[[7,16],[7,18],[12,1],[12,2],[13,13],[14,13],[4,8],[4,14],[4,16],[8,4],[9,16],[9,18],[11,4],[11,12]]
    elif type == 2:
        coordination_list = [[3, 11], [5, 2], [7, 11],[10, 16], [10, 18], [11, 4], [11, 11], [3, 15], [5, 13], [5, 17], [7, 15], [12, 11], [12, 12], [13, 3], [14, 3]]
    elif type == 3:
        coordination_list = [[4, 2], [4, 15], [7, 17], [7, 19], [10, 4], [10, 17], [3, 13], [5, 4], [6, 4], [8, 15], [9, 12], [9, 15], [11, 6], [11, 9], [12, 6] ]
    elif type == 4:
        coordination_list = [[6, 13], [6, 15], [7, 13], [7, 15], [8, 13], [8, 15], [9, 3], [9, 4], [11, 10], [12, 12], [13, 10]]
    elif type == 8:
        coordination_list = [[1, 7], [1, 12], [1, 17], [2, 6], [2, 16], [13, 1], [14, 10], [3, 8], [3, 11], [3, 16], [4, 16], [12, 5], [12, 6], [13, 15], [13, 16]]
    elif type==5:
        while True:
            coordination_list=[[random.randint(1,14),random.randint(1,19)]]
            '''print (coordination_list[0][0]," ",coordination_list[0][1])'''
            if general_terrain[coordination_list[0][0]][coordination_list[0][1]]==api.TerrainType.EMPTY and tower_status[coordination_list[0][0]][coordination_list[0][1]]==False:
                if general_terrain[coordination_list[0][0]+1][coordination_list[0][1]]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]][coordination_list[0][1]+1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]][coordination_list[0][1]-1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]+1][coordination_list[0][1]] in air_system_unit_path or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]] in air_system_unit_path or general_terrain[coordination_list[0][0]][coordination_list[0][1]+1] in air_system_unit_path or general_terrain[coordination_list[0][0]][coordination_list[0][1]-1] in air_system_unit_path or general_terrain[coordination_list[0][0]+1][coordination_list[0][1]] in air_opponent_unit_path or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]] in air_opponent_unit_path or general_terrain[coordination_list[0][0]][coordination_list[0][1]+1] in air_opponent_unit_path or general_terrain[coordination_list[0][0]][coordination_list[0][1]-1] in air_opponent_unit_path:
                    break
    elif type==6:
        while True:
            coordination_list=[[random.randint(1,14),random.randint(1,19)]]
            '''print (coordination_list[0][0]," ",coordination_list[0][1])'''
            if general_terrain[coordination_list[0][0]][coordination_list[0][1]]==api.TerrainType.EMPTY and tower_status[coordination_list[0][0]][coordination_list[0][1]]==False:
                if general_terrain[coordination_list[0][0]+1][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]+1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]+1][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]-1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]+1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]-1]==api.TerrainType.ROAD:
                    print("dev1")
                    break
    elif type==7:
        global try_failure
        try_failure=0
        print("dev4")
        while True:
            global direction_case_for_getting_coordination
            direction_case_for_getting_coordination=-1
            #0= (+1,) 1=(-1,) 2=(,+1) 3=(,-1)
            coordination_list=[[random.randint(1,14),random.randint(1,19)]]
            '''print (coordination_list[0][0]," ",coordination_list[0][1])'''
            if general_terrain[coordination_list[0][0]][coordination_list[0][1]]==api.TerrainType.EMPTY and tower_status[coordination_list[0][0]][coordination_list[0][1]]==False:
                if general_terrain[coordination_list[0][0]+1][coordination_list[0][1]]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]-1][coordination_list[0][1]]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]][coordination_list[0][1]+1]==api.TerrainType.ROAD or general_terrain[coordination_list[0][0]][coordination_list[0][1]-1]==api.TerrainType.ROAD:
                    print("dev5")
                    if general_terrain[coordination_list[0][0]+1][coordination_list[0][1]]==api.TerrainType.ROAD:
                        print("dev7")
                        direction_case_for_getting_coordination=0
                        if general_terrain[coordination_list[0][0]+2][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]+3][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]+4][coordination_list[0][1]]==api.TerrainType.ROAD:
                            print("dev2")
                            break
                        else:
                            try_failure+=1
                    if general_terrain[coordination_list[0][0]-1][coordination_list[0][1]]==api.TerrainType.ROAD:
                        print("dev8")
                        direction_case_for_getting_coordination=1
                        if general_terrain[coordination_list[0][0]-2][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]-3][coordination_list[0][1]]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]-4][coordination_list[0][1]]==api.TerrainType.ROAD:
                            print("dev2")
                            break
                        else:
                            try_failure+=1
                    if general_terrain[coordination_list[0][0]][coordination_list[0][1]+1]==api.TerrainType.ROAD:
                        print("dev9")
                        direction_case_for_getting_coordination=2
                        if general_terrain[coordination_list[0][0]][coordination_list[0][1]+2]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]+3]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]+4]==api.TerrainType.ROAD:
                            print("dev2")
                            break
                        else:
                            try_failure+=1
                    if general_terrain[coordination_list[0][0]][coordination_list[0][1]-1]==api.TerrainType.ROAD:
                        print("dev6")
                        direction_case_for_getting_coordination=3
                        if general_terrain[coordination_list[0][0]][coordination_list[0][1]-2]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]-3]==api.TerrainType.ROAD and general_terrain[coordination_list[0][0]][coordination_list[0][1]-4]==api.TerrainType.ROAD:
                            print("dev2")
                            break
                        else:
                            try_failure+=1
                    if try_failure>=1000:
                        break
    return coordination_list[i]  
def section_2_strategy_selection(type):
    #1= enemy def,2 = enemy atk
    type2_settings()
    if type ==1:
        global current_opponent_side_towers
        counter=0
        for i in range(len(current_opponent_side_towers)):
            if current_opponent_side_towers[i].type==api.TowerType.ICE_LUIGI or current_opponent_side_towers[i].type==api.TowerType.FIRE_MARIO or current_opponent_side_towers[i].type==api.TowerType.SHY_GUY:
                counter+=1
        if counter>=9:
            return True
        else:
            return False
    elif type ==2:
        global current_our_side_enemies
        counter1=0
        counter2=0
        for i in range(len(current_our_side_enemies)):
            if current_our_side_enemies[i].type==api.EnemyType.KOOPA_PARATROOPA or current_our_side_enemies[i].type==api.EnemyType.KOOPA_JR:
                counter1+=1
            else:
                counter2+=1
        if counter1>counter2:
            return True
        else:
            return False
def section_1_implementation():
    type2_settings()
    place_defense()
def section_2_implementation():
    global section_2_case_of_enemy_atk,section_2_case_of_enemy_def
    #===================debug=========
    section_2_case_of_enemy_atk=True
    #enforce it be set to True
    #=================================
    type2_settings()
    if section_2_case_of_enemy_def and section_2_case_of_enemy_atk:
        print("1")
        #def,mario,buzzy
        coordination=get_coordination(5,0)
        if our_money>=400:
            agent.place_tower(api.TowerType.FIRE_MARIO, '1', api.Vector2(coordination[0], coordination[1]))
            tower_status[coordination[0]][coordination[1]]=True
        type2_settings()
        if our_money>=250:
            agent.spawn_unit(api.EnemyType.BUZZY_BEETLE)
    elif section_2_case_of_enemy_def and not section_2_case_of_enemy_atk:
        print("2")
        #def,fort upgrade,buzzy
        upgrade_defense()
        type2_settings()
        if our_money>=250:
            agent.spawn_unit(api.EnemyType.BUZZY_BEETLE)
    elif not section_2_case_of_enemy_def and section_2_case_of_enemy_atk:
        print("3")
        #atk,mario,paratroopa
        type2_settings()
        if our_money>=250:
            agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
        coordination=get_coordination(5,0)
        type2_settings()
        if our_money >=400:
            agent.place_tower(api.TowerType.FIRE_MARIO, '1', api.Vector2(coordination[0], coordination[1]))
            tower_status[coordination[0]][coordination[1]]=True
    elif not section_2_case_of_enemy_def and not section_2_case_of_enemy_atk:
        print("4")
        #atk,fort upgrade,paratroopa
        type2_settings()
        if our_money>=250:
            agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
        type2_settings()
        upgrade_defense()
def section_3_implementation():
    type2_settings() 
    if our_money>=250:
        agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
    type2_settings()
    if our_money>=250:
        agent.spawn_unit(api.EnemyType.KOOPA_PARATROOPA)
    type2_settings()
    if our_money>=250:
        agent.spawn_unit(api.EnemyType.BUZZY_BEETLE)
    type2_settings()
    if our_money>=500:
        agent.spawn_unit(api.EnemyType.WIGGLER)
    type2_settings()
    if our_money>=250:
        agent.spawn_unit(api.EnemyType.SPINY_SHELL)
    type2_settings()
    if our_money>=100:
        agent.spawn_unit(api.EnemyType.GOOMBA)
    type2_settings()
    if our_money>=3000:
        agent.spawn_unit(api.EnemyType.KOOPA_JR)
    type2_settings()
    if our_money>=3000:
        agent.spawn_unit(api.EnemyType.KOOPA)
    type2_settings()
def use_spells():
    type2_settings()

    #cast double income as soon as possible
    agent.cast_spell(api.SpellType.DOUBLE_INCOME)

    #cast teleport at the beginning of the game,after wave6 start cast it as soon as possible
    teleport_target = agent.get_system_path(False)[0]
    if current_wave == 2:
        agent.cast_spell(api.SpellType.TELEPORT, teleport_target)
    elif current_wave >= 6:
        teleport_cooldown = agent.get_spell_cooldown(True,api.SpellType.TELEPORT)
        if teleport_cooldown == 0:
            agent.cast_spell(api.SpellType.TELEPORT, teleport_target)

    poison_cooldown = agent.get_spell_cooldown(True,api.SpellType.POISON)
    if poison_cooldown == 0:
        for enemy in current_our_side_enemies:
            progress_ratio = enemy.progress_ratio
            poison_target =  enemy.position
            if progress_ratio > 0.75 and enemy.type!=api.EnemyType.KOOPA_PARATROOPA:
                agent.cast_spell(api.SpellType.POISON, poison_target)

type2_settings()
type1_settings(general_terrain)

while True:
    global disconect_used_times
    type2_settings()
    if current_wave%2!=0 and current_wave != -1:
        if current_wave==3 and disconect_used_times==0 or current_wave==5 and disconect_used_times==1 or current_wave==7 and disconect_used_times==2 or current_wave==9 and disconect_used_times==3 or current_wave==11 and disconect_used_times==4:
            try:
                agent.disconnect()
                disconect_used_times+=1
            except:
                pass
    #========
    try:
        agent.super_star()
    except:
        pass
    try:
        agent.turbo_on()
    except:
        pass
    #=========
    #section identify   
    #sec1=4 waves,sec2=4 waves,sec3=3 waves 
    type2_settings()
    if current_wave<5:
        current_section=1
    elif current_wave<9:
        current_section=2
    else:
        current_section=3
    
    #section2 pre-check
    global one_time_check_1
    if current_section==2 and not one_time_check_1:
        section_2_case_of_enemy_def=section_2_strategy_selection(1)
        #True=opponent adopted anti air strategy
        section_2_case_of_enemy_atk=section_2_strategy_selection(2)
        #True=opponent adopted air force strategy
        one_time_check_1=True
        print (section_2_case_of_enemy_def,section_2_case_of_enemy_atk)
    use_spells()
    type2_settings()
    if current_section==1:
        section_1_implementation()
    elif current_section==2:
        section_2_implementation()
    elif current_section==3:
        section_3_implementation()