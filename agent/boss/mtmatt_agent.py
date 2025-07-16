# Copyright © 2025 mtmatt. All rights reserved.

import os
import sys
from api_importer import *
import random

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = True


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


agent = GameClient(7749, "TOKEN")  # Replace with actual token
agent.set_name("mtmatt")

agent.pixelcat()

debug("========== Terrain  ==========")
terrain = agent.get_all_terrain()
# terrain = [list(row) for row in zip(*terrain)]
for row in terrain:
    for t in row:
        debug(f"{t.value:2d}", end=" ")
    debug()
debug("==============================")

# Get the path of the enemies


def check_path(path) -> bool:
    if not isinstance(path, list):
        return False
    return True


def get_sorted_cell():
    enemy_pathes = [None, None, None, None]

    while not check_path(enemy_pathes[0]):
        enemy_pathes[0] = agent.get_system_path(True)
    while not check_path(enemy_pathes[1]):
        enemy_pathes[1] = agent.get_opponent_path(True)
    while not check_path(enemy_pathes[2]):
        enemy_pathes[2] = agent.get_system_path(False)
    while not check_path(enemy_pathes[3]):
        enemy_pathes[3] = agent.get_opponent_path(False)
    
    freq = {}
    for enemy_path in enemy_pathes:
        for cell in enemy_path:
            if (cell.x, cell.y) not in freq:
                freq[(cell.x, cell.y)] = 0
            freq[(cell.x, cell.y)] += 1
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    sorted_path = []
    for cell, count in freq:
        sorted_path.append(Vector2(cell[0], cell[1]))

    debug("========== Enemy Paths ==========")
    for cell in sorted_path:
        debug(f"({cell.x}, {cell.y})", end=" ")
    debug("\n=================================")

    # Find path surrounding
    sorted_cells = []
    for enemy_path in enemy_pathes:
        for cell in enemy_path:
            shift = [Vector2(0, 0),
                Vector2(0, 1), Vector2(1, 0), Vector2(0, -1), Vector2(-1, 0), Vector2(1, 1), Vector2(1, -1),
                Vector2(-1, 1), Vector2(-1, -1),
                # Vector2(2, 0), Vector2(0, 2), Vector2(-2, 0), Vector2(0, -2)
                ]
            for offset in shift:
                pos = Vector2(cell.x + offset.x, cell.y + offset.y)
                if 0 < pos.x <= 14 and 0 < pos.y <= 19:
                    sorted_cells.append(pos)

    # Sort by frequency similar to the path cells above
    freq_cells = {}
    for cell in sorted_cells:
        if (cell.x, cell.y) not in freq_cells:
            freq_cells[(cell.x, cell.y)] = 0
        freq_cells[(cell.x, cell.y)] += 1

    freq_cells = sorted(freq_cells.items(), key=lambda x: x[1], reverse=True)
    sorted_cells = []
    for cell, count in freq_cells:
        sorted_cells.append(Vector2(cell[0], cell[1]))

    return sorted_cells


sorted_cells = get_sorted_cell()
debug("========== Sorted cells =========")
for cell in sorted_cells:
    debug(f"{cell}", end=" ")
debug("\n=================================")

while True:
    current_money = agent.get_money(True)
    current_income = agent.get_income(True)

    # Double income if possible
    if agent.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) == 0:
        agent.cast_spell(SpellType.DOUBLE_INCOME)

    # Try to spawn any available unit
    try:
        if agent.get_remain_time() > 45:
            agent.spawn_unit(EnemyType.GOOMBA)
            agent.spawn_unit(EnemyType.BUZZY_BEETLE)
            agent.spawn_unit(EnemyType.KOOPA_PARATROOPA)
            agent.spawn_unit(EnemyType.SPINY_SHELL)
    except ApiException as e:
        debug(f"Failed to spawn unit: {e}")

    # Update the optimal tower placement
    sorted_cells = get_sorted_cell()

    # If we have enough money, place towers
    all_towers = agent.get_all_towers(True)
    if current_money >= 3300 and current_income >= 300:
        for cell in sorted_cells:
            can_place = True
            for placed_tower in all_towers:
                print(
                    f"Checking {placed_tower.position} against {cell}: {placed_tower.position.__str__() == cell.__str__()}")
                if placed_tower.position.__str__() == cell.__str__():
                    can_place = False
                    break
            if not can_place:
                continue
            try:
                viable_towers = [
                    TowerType.FIRE_MARIO,
                    TowerType.ICE_LUIGI
                ]
                random.shuffle(viable_towers)

                agent.place_tower(viable_towers[0], "3a", cell)
                debug(f"Placed Tower at {cell}")
            except ApiException as e:
                debug(f"Failed to place tower: {e}")

    # If we have too much money, send Koopa
    if current_money >= 10000 and agent.get_remain_time() > 30:
        try:
            agent.spawn_unit(EnemyType.KOOPA_JR)
            agent.spawn_unit(EnemyType.KOOPA)
        except ApiException as e:
            debug(f"Failed to spawn Koopa: {e}")
