# Copyright © 2025 mtmatt. All rights reserved.

import api 

agent = api.GameClient(7749, 'TOKEN')

while True:
    remain_time = agent.get_remain_time()
    
    # CAST DOUBLE INCOME
    income_multiplier: int = 1
    agent.cast_spell(api.SpellType.DOUBLE_INCOME)
    income_multiplier = 2

    # INCOME ENHANCEMENT
    if agent.get_income(True) / income_multiplier < 150:
        agent.spawn_unit(api.EnemyType.GOOMBA)
    elif len(agent.get_all_towers(True)) > 20 and agent.get_income(True) / income_multiplier < 250:
        agent.spawn_unit(api.EnemyType.GOOMBA)

    # DEFENSE
    terrain = agent.get_all_terrain()
    for (row, data) in enumerate(terrain):
        for (col, tile) in enumerate(data):
            if tile == api.TerrainType.EMPTY:
                agent.place_tower(api.TowerType.FIRE_MARIO, '1', api.Vector2(row, col))

    # ATTACK
    if agent.get_money(True) >= 3000:
        agent.spawn_unit(api.EnemyType.KOOPA_JR)

    # CHAT
    agent.send_chat('你說飛行敵人太強，其實是你太習慣凡事都想一步解決。')
