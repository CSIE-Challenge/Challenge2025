import time
import api_importer as api
from test_token import TOKEN1, TOKEN2


def print_chat(agent, count):
    print("Chat History:")
    hist = agent.get_chat_history(count)
    if isinstance(hist, api.ApiException):
        print(hist)
    else:
        for i in hist:
            print(i)


agent1 = api.GameClient(7749, TOKEN1)
agent2 = api.GameClient(7749, TOKEN2)

print("API call...", agent1.set_name("PixelCat"))
print("API call...", agent1.set_chat_name_color("1f1e33"))
print("API call...", agent2.set_name("HyperSoGoat"))  # too long
print("API call...", agent2.set_name("HyperGoat"))
print("API call...", agent2.set_chat_name_color("ff69b4"))

print("Sending chat...", agent1.send_chat("adsflkjhasdflkjahsdflkjh"))
time.sleep(2.1)
print("Sending chat...", agent1.send_chat("起來，不願做奴隸的人們"))
time.sleep(2.1)
print("Sending chat...", agent2.send_chat("喵喵喵喵喵喵喵喵"))
time.sleep(2.1)
print("Sending chat...", agent1.send_chat("٩(ˊᗜˋ*)و"))
time.sleep(2.1)
print("Sending chat...", agent2.send_chat("Arch addicted :yum:"))
time.sleep(2.1)

print_chat(agent1, 3)

# esteregg
agent2.set_chat_name_color("hyper")
agent2.send_chat("SUS")
print_chat(agent2, 5)
