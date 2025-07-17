import api_importer as api
from test_token import TOKEN1

INVOKE_COUNT = 500

agent = api.GameClient(7749, TOKEN1)

pixel_cat = agent.pixelcat()
print(pixel_cat)
pixel_cat = agent.pixelcat()
print(pixel_cat)
print(
    agent.send_chat(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
)
print(agent.send_chat("ouo ouo"))
