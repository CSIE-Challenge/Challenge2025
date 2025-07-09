import time
from api import *

api = GameClient(7749)

print(api.get_scores(True))
print(api.get_scores(False))
print(api.get_current_wave())
start = time.perf_counter()
for _ in range(10):
    towers = api.get_all_towers(True)  # 獲取玩家自己的所有塔
    for tower in towers:
        print(tower)

end = time.perf_counter()
elapsed = end - start
print(f"Elapsed time: {elapsed:.6f} seconds")
