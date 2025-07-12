import time
from api import *

api = GameClient(7749, "b32184f9")

ret = api.get_system_path(False)
ret2 = api.get_system_path(False)
if isinstance(ret2, ApiException):
    print(ret2)
else:
    for cell in ret2:
        print(f"({cell.x}, {cell.y})")

