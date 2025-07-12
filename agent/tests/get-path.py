from api import *

api = GameClient(7749, "TOKEN")

sys_fly = api.get_system_path(True)
sys_ground = api.get_system_path(False)
opp_fly = api.get_opponent_path(True)
opp_ground = api.get_opponent_path(False)

if isinstance(sys_fly, ApiException) or isinstance(sys_ground, ApiException) or isinstance(opp_fly, ApiException) or isinstance(opp_ground, ApiException):
    print("bruh")
else:
    print(f"Begin: ({sys_fly[0].x}, {sys_fly[0].y}), end: ({sys_fly[-1].x}, {sys_fly[-1].y})")
    print(f"Begin: ({sys_ground[0].x}, {sys_ground[0].y}), end: ({sys_ground[-1].x}, {sys_ground[-1].y})")
    print(f"Begin: ({opp_fly[0].x}, {opp_fly[0].y}), end: ({opp_fly[-1].x}, {opp_fly[-1].y})")
    print(f"Begin: ({opp_ground[0].x}, {opp_ground[0].y}), end: ({opp_ground[-1].x}, {opp_ground[-1].y})")

print([str(i) for i in sys_fly])
print([str(i) for i in sys_ground])
print([str(i) for i in opp_fly])
print([str(i) for i in opp_ground])
