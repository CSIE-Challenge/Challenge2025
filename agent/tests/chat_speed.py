import api
import time

agent1 = api.GameClient(7749, "fd166fe1")
agent2 = api.GameClient(7749, "3327ed42")

print("API call...", agent1.set_name("PixelCat"))
print("API call...", agent1.set_chat_name_color("1f1e33"))
print("API call...", agent2.set_name("HyperSoGoat"))
print("API call...", agent2.set_chat_name_color("ff69b4"))

while True:
    agent1.send_chat("111")
    agent2.send_chat("222")
    time.sleep(1)