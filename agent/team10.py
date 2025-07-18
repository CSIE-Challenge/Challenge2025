import time
import random
from api import Tower
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource

cc = False
set_total = 0
get_total = 0

agent = GameClient(7749, "bb465d69")  # Replace with your token

# 全域通行頂級榮耀特選尊貴專屬至尊終身極享體驗限量貴賓卡api
agent.set_the_radiant_core_of_stellar_faith(100)

get_total = agent.get_the_radiant_core_of_stellar_faith()

# 貴賓卡api判斷

while get_total >= 400:
    if get_total >= 4500:
       agent.ntu_student_id_card()
    elif get_total >= 2500:
        cc = True
    elif get_total >= 400:
        agent.metal_pipe()

# ----------chat log----------
# 設定名稱與顏色

agent.set_name("10")
agent.set_chat_name_color("A2CFFE")

# 聊天訊息清單

chat_logs = [
    "不會寫Challenge，為什麼不找找自己問題",
    "首先我先恭喜你，你被我恭喜了",
    "如果我沒猜錯的話，那我應該猜對的",
    "秦始皇騎北極熊，北極熊騎秦始皇",
    "你真的很糖欸",
    "小美人魚是什麼系的？under the sea",
    "那一天的憂鬱，憂鬱起來。那一天的寂寞，寂寞起來。",
    "我們在俠盜獵車手6之前得到了台大Challenge作業，沒有路",
    "你知道北極皇為什麼要騎秦始熊嗎？因為我也不知道",
    "越來越愛你Challenge",
    "Challenge你別佔有我",
    "打一輩子的Challenge",
    "never gonna give you up",
    "我愛木須龍啦",
    "我愛慕虛榮啦",
    "為什麼要演奏春日影",
    "是又怎樣",
    "艾倫走路者傳說，我們生活，我們愛，我們說謊:musical_note::notes::musical_note:",
    "你竟敢無視燈",
    "來都來了，來寫Challenge吧",
    "早上好台大，現在我有Challenge", 
    "胡允升好帥！！！",
    "林筠臻是全系最漂亮的學姊ovo"
    "拒絕草莓可樂從你我做起",
    "猿神啟動",
    "我的豆花！！！30塊！！！！！",
    "www",
    "wwwwwwww",
    "雙眼皮= = 單眼皮- -",
    "香菜，狗都不吃",
    "ᕕ(◠ڼ◠)ᕗ",
    "我家的Challenge 會後空翻",
    "比遊戲還刺激？是Challenge 喔？",
    "114514，這麼臭的數字有必要存在嗎？",
    "熬夜打Challenge，如果是勇者欣梅爾的話一定會這麼做的",
    
]

# -----------預防disconnected但是沒寫出來所以變"global的變數初始化"-----------

tower = 0
up_grade = 0
all_place1 = []
all_place2 = []

# ----------檢查該點為是否為敵人路徑(結合後方的程式檢查是否為敵任路徑旁的格子點)----------

def is_path(x, y):
    global opponent, system
    for pos in opponent:
        if pos.x == x and pos.y == y : 
            return True
    for pos in system:
        if pos.x == x and pos.y == y : 
            return True
    return False

# ----------獲得敵人會經過的所有路徑，記錄在overlap_coor、opponent跟system----------
system = agent.get_system_path(False) # 系統指派的敵人經過路徑
opponent = agent.get_opponent_path(False) # 對手指派敵人的經過路徑

is_overlap = False
overlap_coor = Vector2(0, 0)
find = False

for i in system:
    if find:
        break
    for j in opponent:
        if i.x == j.x and i.y == j.y:
            overlap_coor = Vector2(i.x, i.y)
            find = True
            break


# ----------根據敵人經過的路徑排序好放塔的陣列----------
terrain = agent.get_all_terrain()
all_place_count = 0

for i in range(15):
    for j in range(20):
        if terrain[i][j] == TerrainType.EMPTY : # 確定當格是能夠放塔的格子

            # 確認附近是否有敵人路徑
            if is_path(i + 1, j) or is_path(i - 1, j) or is_path(i, j + 1) or is_path(i, j - 1):
                all_place_count += 1

                # 插入到最中間
                all_place1.insert( 0, Vector2(i, j)) 

# ----------主迴圈----------
cut = False
return_ = False
GOOMBA = 0
start_time = time.time()
max_duration = 280  # 最多執行 280 秒


while True:
    # -----------reset-----------

    remain_time = agent.get_remain_time()
    money = agent.get_money(True)
    income = agent.get_income(True)

    # disconnected對手
    if remain_time <= 160 and cc == True: 
        agent.disconnect()

    # 獲得最前面的敵人座標
    all_enemies = agent.get_all_enemies(True)  # 獲取自己地圖上所有敵人的資訊
    enemy_coor = None
    if all_enemies:
        enemy_coor = all_enemies[0].position  # 獲取最前面敵人座標

    # ----------三種效果使用----------
    # double income
    if agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) == 0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)

    # poison
    if agent.get_spell_cooldown(True, SpellType.POISON) == 0 and remain_time <= 297 :
        agent.cast_spell(SpellType.POISON, overlap_coor)

    # tp
    if agent.get_spell_cooldown(True, SpellType.TELEPORT) == 0 and remain_time<=297 and enemy_coor is not None:
        enemy_coor = all_enemies[0].position  # 獲取最前面敵人座標
        agent.cast_spell(SpellType.TELEPORT, enemy_coor)

    # ----------chat----------

    # 時間到了就跳出
    if remain_time <= 0:
        break

    # 聊天觸發邏輯：隨機發話
    if time.time() - start_time < max_duration:
        if random.random() < 0.1:  # 10% 機率發話（避免過快）
            agent.send_chat(random.choice(chat_logs))

    # -----------放置防禦塔----------- #
    total_tower = agent.get_all_towers(True)
    tower_count = len(total_tower)
    total_mario = 0

    # 確定場上的全部mario數量
    for i in range(tower_count):
        if total_tower[i].type == TowerType.FIRE_MARIO:
            total_mario += 1

    # 放置第一個mario
    if money >= 400 and tower_count == 0:
        agent.place_tower(TowerType.FIRE_MARIO, '1', all_place1[0])
        all_place2.append(all_place1[0])

    else:
        # 在income > 100之前持續派栗寶寶
        if income < 100 :
            if money >= 100 and GOOMBA <= 5:
                agent.spawn_unit(EnemyType.GOOMBA)
                GOOMBA += 1
         
        if GOOMBA >= 5 :
            #在放置5座mario後持續派栗寶寶
            if tower_count >= 5 :
                if money >= 100:
                    agent.spawn_unit(EnemyType.GOOMBA) # 派栗寶寶
                    GOOMBA += 1

            if remain_time >= 210:
                # 在210秒前指派1階火焰瑪莉歐
                if money >= 400:
                    agent.place_tower(TowerType.FIRE_MARIO, '1', all_place1[0])

                    #將all_place1的座標移至all_place2記錄下來，確保後續升級
                    all_place2.append(all_place1[0])
                    all_place1.pop(0)

            else:

                # 當總塔數>=10且準備升級的list裡面不為空時升級
                if money >= 2600 and tower_count >= 10 and len(all_place2) > 0:

                    # 路易吉跟嘿呵輪流生成
                    if return_ == False:
                        agent.place_tower(TowerType.SHY_GUY, '3b', all_place2[0])
                        return_ = True
                    else:
                        agent.place_tower(TowerType.ICE_LUIGI, '3b', all_place2[0])
                        return_ = False
                    up_grade += 1
                    all_place2.pop(0)
                    
            if money >= 400 and up_grade >= 6 and len(all_place1) > 0 :
                    agent.place_tower(TowerType.FIRE_MARIO, '1', all_place1[0])
                    all_place2.append(all_place1[0])
                    all_place1.pop(0)
            
            if len(all_place1) <= 0 or remain_time <= 60 :
                if money >= 2800 and up_grade >= 10 :

                    # 在地圖上隨機一個空點生成嘿呵
                    find = False
                    for (row, data) in enumerate(terrain):
                        if find:
                            break
                        for (col, tile) in enumerate(data):
                            if tile == TerrainType.EMPTY:
                                agent.place_tower(TowerType.SHY_GUY, '3a', Vector2(row, col))
                                find = True
                                break
                                
                if money >= 400 :

                    # 在地圖上的隨機一個地方生成1階瑪莉歐
                    find = False
                    for (row, data) in enumerate(terrain):
                        if find:
                            break
                        for (col, tile) in enumerate(data):
                            if tile == TerrainType.EMPTY:
                                agent.place_tower(TowerType.FIRE_MARIO, '1', Vector2(row, col))
                                find = True
                                break