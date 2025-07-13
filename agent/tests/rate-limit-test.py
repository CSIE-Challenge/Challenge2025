import time
import api_importer as api
from test_token import TOKEN1

INVOKE_COUNT = 500

agent = api.GameClient(7749, TOKEN1)

start = time.perf_counter()
for _ in range(INVOKE_COUNT):
    assert not isinstance(agent.get_game_status(), api.ApiException)
end = time.perf_counter()
elapsed = end - start

print(f"API request count: {INVOKE_COUNT}")
print(f"Elapsed time: {elapsed:.6f} seconds")
print(f"Time per request: {elapsed / INVOKE_COUNT:.6f} seconds")
print(f"Request per second: {INVOKE_COUNT / elapsed:.6f} seconds")
