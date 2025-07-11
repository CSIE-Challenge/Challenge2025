import time
from api import *

api = GameClient(7749, "53f4d2a1")

while True:
    print(api.get_game_status())
    time.sleep(2)