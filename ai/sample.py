import time
from api import *

api = GameClient(7749)

print(api.get_scores(True))
print(api.get_scores(False))
print(api.get_current_wave())
start = time.perf_counter()
for _ in range(10):
    exist = api.get_tower(Vector2(8, 4))
    print(exist)

end = time.perf_counter()
elapsed = end - start
print(f"Elapsed time: {elapsed:.6f} seconds")
