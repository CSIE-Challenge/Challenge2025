import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from time import sleep
from api import *

api = GameClient(7749, "ef80319c")

PRICE = [40, 10, 60, 20, 70, 30, 50]
init_income = 10
target_income = 18

for enemy in EnemyType:
  while api.get_money(True) < PRICE[enemy]:
    sleep(1)
  api.spawn_unit(enemy)

cur_income = api.get_income(True)

if (cur_income != target_income):
  api.send_chat(f"[income_change] Test failed, cur: {cur_income}, target: {target_income}")
else:
  api.send_chat(f"[income_change] Test passed.")