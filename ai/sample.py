from api import GameClient

api = GameClient(7749)

# print(api.get_scores(48763))
# raise api.get_scores(False)

import time
start = time.perf_counter()
for _ in range(200):
    api.get_all_terrain()
end = time.perf_counter()
elapsed = end - start
print(f"Elapsed time: {elapsed:.6f} seconds")
