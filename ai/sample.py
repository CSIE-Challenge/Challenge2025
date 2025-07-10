import time
from api import *

api = GameClient(7749, "04350561")

while True:
    status = api.get_game_status()
    print(type(status), status, status.name)
    time.sleep(2)