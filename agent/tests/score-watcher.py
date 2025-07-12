import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
import api

agent = api.GameClient(7749, "TOKEN")

while True:
    print(agent.get_scores(True))
    time.sleep(0.5)
