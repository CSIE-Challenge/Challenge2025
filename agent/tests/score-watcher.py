import time
import api_importer as api
from test_token import TOKEN1

agent = api.GameClient(7749, TOKEN1)

while True:
    print(agent.get_scores(True))
    time.sleep(0.5)
