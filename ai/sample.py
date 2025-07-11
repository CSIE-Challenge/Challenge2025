import time
from api import *

api = GameClient(7749, "31ceb514")

while True:
    print(api.get_game_status())
    time.sleep(2)