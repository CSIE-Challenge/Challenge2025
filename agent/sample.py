import time
from api import *

api = GameClient(7749, "b32184f9")

ret = api.get_system_path(True)
if isinstance(ret, ApiException):
    print(ret)
else:
    for cell in ret:
        print(f"({cell.x}, {cell.y})")

