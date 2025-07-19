# Copyright © 2025 mtmatt, ouo. All rights reserved. 
 
import time 
from api import GameClient, GameStatus, Vector2, TowerType, TargetStrategy, EnemyType, SpellType, TerrainType, ChatSource 
 
agent = GameClient(7749, "361b9eda")  # Replace with你的token 
 
print("Waiting for game to RUNNING...") 
while agent.get_game_status() != GameStatus.RUNNING: 
    time.sleep(0.5) 
print("Game RUNNING!\n") 
 
# 先打印基本資訊 
print("Scores:", agent.get_scores(True), "(Me) /", agent.get_scores(False), "(Opp)") 
print("Money: ", agent.get_money(True), "(Me) /", agent.get_money(False), "(Opp)") 
print("Income:", agent.get_income(True), "(Me) /", agent.get_income(False), "(Opp)\n") 
 
print("Wave:", agent.get_current_wave()) 
print("Remain time:", f"{agent.get_remain_time():.2f}s") 
print("Until next wave:", f"{agent.get_time_until_next_wave():.2f}s\n") 
 
# 設定聊天名稱 
agent.set_name("OuO") 
agent.set_chat_name_color("DCB5FF") 
agent.send_chat("OuO is going full offense! >:D") 
 

terrain_map = agent.get_all_terrain()
start_pos = None
end_pos = None


# 測試印出
print("起點座標 =", start_pos)
print("終點座標 =", end_pos)
           
terrain = agent.get_all_terrain()
# 主要進攻迴圈 
while True: 
    # 確保遊戲還在跑 
    if agent.get_game_status() != GameStatus.RUNNING: 
        print("Game ended!") 
        break 
 
    # CAST DOUBLE INCOME（只有冷卻完成才施放） 
    if agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) == 0: 
        agent.cast_spell(SpellType.DOUBLE_INCOME) 
        print("💰 施放雙倍收入法術！") 
 
    # 取得基礎收入（排除雙倍加成） 
    income_multiplier = 2 if agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) > 0 else 1 
    current_income = agent.get_income(True) / income_multiplier 
 
     
    
    # === 進攻策略 === 
    money = agent.get_money(True) 
    nowtime = agent.get_remain_time()

    if money >= 100 and agent.get_remain_time()>=90: 
        agent.spawn_unit(EnemyType.GOOMBA) 
        
    money = agent.get_money(True) 
 
    if money >= 250 and agent.get_remain_time()>=60: 
        agent.spawn_unit(EnemyType.BUZZY_BEETLE) 
    money = agent.get_money(True) 
 
    if money >= 250: 
        agent.spawn_unit(EnemyType.KOOPA_PARATROOPA) 
    money = agent.get_money(True) 
 
    if money >= 250: 
        agent.spawn_unit(EnemyType.SPINY_SHELL) 
    money = agent.get_money(True) 
 
    if money >= 500: 
        agent.spawn_unit(EnemyType.WIGGLER) 
    money = agent.get_money(True) 
 
    if money >= 3000: 
        agent.spawn_unit(EnemyType.KOOPA_JR) 
    money = agent.get_money(True) 
 
    if money >= 3000: 
        agent.spawn_unit(EnemyType.KOOPA) 

 
    # === 進攻型法術（例：毒）=== 
    enemy_path = agent.get_system_path(False)
    if enemy_path:
        enemy_first_pos = enemy_path[0] 
        enemy_end_pos = enemy_path[-1]

    if agent.get_spell_cooldown(True, SpellType.POISON) == 0: 
        agent.cast_spell(SpellType.POISON, enemy_first_pos) 
        print("☠️ 施放毒法術干擾對手！")
    if agent.get_spell_cooldown(True, SpellType.TELEPORT) == 0 and agent.get_remain_time()<=250: 
        agent.cast_spell(SpellType.TELEPORT, enemy_end_pos) 
        print("☠️ 施放毒法術干擾對手！") 
    
    if money > 7000:
        for x in range(0,15):
            for y in range(0,20):
                if((terrain[x][y]==1 and terrain[x][y+1]==2 )or (terrain[x][y]==1 and terrain[x+1][y]==2)):
                    pos = Vector2(x,y)
                    if agent.get_tower(True, pos) is None:
                        print("No tower at", pos, "→ placing FIRE_MARIO lvl 1")
                        agent.place_tower(TowerType.DONKEY_KONG, "3a", pos)
    

    # # === 偶爾聊天挑釁 XD ===

    from random import randint, choice
    def chat(word_list):
        return choice(word_list)
    agent.set_name('緯大砲')
    agent.set_chat_name_color("FFFFFF")
    word_list = ['欸 這房間是訓練模式',
                    '你們的程式像是從sample裡複製下來的',
                    '等等，別生氣。我這邊有提供教學連結',
                    '看你們的操作連滑鼠都在反抗',
                    '你這波操作是來笑死我還是打贏我？我分不清了。',
                    '你還在玩，我已經洗完澡、泡了茶、你的基地還沒爆，我替它難過。',
                    '你進來是自願的嗎？還是有人脅迫你來獻祭智商的？',
                    '你們的兵跟豆腐一樣，一踩就碎，還沒調味。',
                    '這不是操作失誤，這是設計缺陷——你設計的那顆腦。',
                    '你死得那麼快，是不是遊戲的預設劇情啊？',
                    '你防線比我期末分數還低。',
                    '人字拖對足控來說算不算比基尼 ?',
                    '你是不是畫質太低，所以看不到你快輸了?',
                    '打你們跟打落單的候鳥一樣沒有南渡。']

    agent.send_chat(chat(word_list))

    if (500-agent.get_remain_time() == 60):
        agent.send_chat('為什麼美國人玩傳說對決都會輸？ \n\n\n 因為他們開局就少兩座塔。（911)')
    if (500-agent.get_remain_time() == 180) :
        agent.send_chat('你知道黑人跟枕頭的共通點是什麼嗎？ \n\n\n 你打的越用力，產出的棉花就越多。')
    if (500-agent.get_remain_time() == 240) :
        agent.send_chat('各位知道如何委婉地說大便這個詞嗎？ \n\n\n 拉BuBu。')