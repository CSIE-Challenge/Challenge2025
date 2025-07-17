import api_importer as api
from test_token import TOKEN1, TOKEN2
import time

agent1 = api.GameClient(7749, TOKEN1)
agent2 = api.GameClient(7749, TOKEN2)

print("API call...", agent1.set_name("PixelCat"))
print("API call...", agent1.set_chat_name_color("1f1e33"))
print("API call...", agent2.set_name("HyperSoGoat"))
print("API call...", agent2.set_chat_name_color("ff69b4"))

while True:
    agent1.send_chat("111")
    agent2.send_chat("222")
    time.sleep(1)