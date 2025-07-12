import time
import api_importer as api

agent = api.GameClient(7749, "350a5458")

while True:
    print(agent.get_scores(True))
    time.sleep(0.5)
