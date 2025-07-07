from api import GameClient

client = GameClient(7749)

input()
print(client.get_scores(True))
print(client.get_all_terrain())
print(client.get_scores(False))
