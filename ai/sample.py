import time
from api import *

api = GameClient(7749)

print(api.get_scores(True))
print(api.get_scores(False))

start = time.perf_counter()
for _ in range(500):
    #ret = api.get_all_terrain()
    #if isinstance(ret, ApiException):
    #    print(ret)
    print("a")
    api.send_chat("123")
    time.sleep(0.5)

end = time.perf_counter()
elapsed = end - start
print(f"Elapsed time: {elapsed:.6f} seconds")
