import time
from api import *

api = GameClient(7749)

print(api.get_money(True))
print(api.get_money(False))

start = time.perf_counter()
# for _ in range(500):
#     ret = api.get_all_terrain()
#     if isinstance(ret, ApiException):
#         print(ret)
end = time.perf_counter()
elapsed = end - start
print(f"Elapsed time: {elapsed:.6f} seconds")
