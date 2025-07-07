from api import GameClient

api = GameClient(7749)

input()
print(api.get_scores(True))
print(api.get_scores(False))
print(api.get_all_terrain())
