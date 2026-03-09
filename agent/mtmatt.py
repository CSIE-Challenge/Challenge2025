# Copyright Â© 2025 mtmatt. All rights reserved.

import os
import sys
from api import *
import random

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

DEBUG = False


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


client = GameClient(7749, "c7761b10")  # Replace with actual token
client.set_name("mtmatt")

client.pixelcat()

debug("========== Terrain  ==========")
terrain = client.get_all_terrain()
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
        enemy_pathes[0] = client.get_system_path(True)
    while not check_path(enemy_pathes[1]):
        enemy_pathes[1] = client.get_opponent_path(True)
    while not check_path(enemy_pathes[2]):
        enemy_pathes[2] = client.get_system_path(False)
    while not check_path(enemy_pathes[3]):
        enemy_pathes[3] = client.get_opponent_path(False)
    
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
    current_money = client.get_money(True)
    current_income = client.get_income(True)

    # Double income if possible
    if client.get_spell_cooldown(True, SpellType.DOUBLE_INCOME) == 0:
        client.cast_spell(SpellType.DOUBLE_INCOME)

    all_enemies = client.get_all_enemies(True)
    if client.get_spell_cooldown(True, SpellType.POISON) == 0:
        cells = {}
        for enemy in all_enemies:
            if (enemy.position.x, enemy.position.y) not in cells:
                cells[(enemy.position.x, enemy.position.y)] = 0
            cells[(enemy.position.x, enemy.position.y)] += 1
        if len(cells) > 0:
            cell_with_most_enemies = max(cells, key=cells.get)
            if cells[cell_with_most_enemies] > 4:
                client.cast_spell(SpellType.POISON, Vector2(cell_with_most_enemies[0], cell_with_most_enemies[1]))
    
    if client.get_spell_cooldown(True, SpellType.TELEPORT) == 0:
        cells = {}
        for enemy in all_enemies:
            if (enemy.position.x, enemy.position.y) not in cells:
                cells[(enemy.position.x, enemy.position.y)] = 0
            cells[(enemy.position.x, enemy.position.y)] += enemy.damage
        if len(cells) > 0:
            cell_with_most_enemies = max(cells, key=cells.get)
            if cells[cell_with_most_enemies] > 6000:
                client.cast_spell(SpellType.TELEPORT, Vector2(cell_with_most_enemies[0], cell_with_most_enemies[1]))


    # Try to spawn any available unit
    try:
        if client.get_remain_time() > 45:
            client.spawn_unit(EnemyType.GOOMBA)
        if client.get_remain_time() > 60:
            client.spawn_unit(EnemyType.BUZZY_BEETLE)
            client.spawn_unit(EnemyType.KOOPA_PARATROOPA)
            client.spawn_unit(EnemyType.SPINY_SHELL)
    except ApiException as e:
        debug(f"Failed to spawn unit: {e}")

    # Update the optimal tower placement
    sorted_cells = get_sorted_cell()

    # If we have enough money, place towers
    all_towers = client.get_all_towers(True)
    if current_money >= 3300 and current_income >= 300:
        for cell in sorted_cells:
            can_place = True
            for placed_tower in all_towers:
                debug(
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

                client.place_tower(viable_towers[0], "3a", cell)
                debug(f"Placed Tower at {cell}")
            except ApiException as e:
                debug(f"Failed to place tower: {e}")

    # If we have too much money, send Koopa
    if len(all_towers) > 25 and client.get_remain_time() > 30:
        try:
            client.spawn_unit(EnemyType.KOOPA_JR)
            client.spawn_unit(EnemyType.KOOPA)
        except ApiException as e:
            debug(f"Failed to spawn Koopa: {e}")