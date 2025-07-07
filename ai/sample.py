from api import GameClient

api = GameClient(7749)

print(api.get_scores(48763))
raise api.get_scores(False)
# print(api.get_all_terrain())
