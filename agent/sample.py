import time
from api import *

api = GameClient(7749, "b32184f9")

ret = api.get_system_path()
if isinstance(ret, ApiException):
    print("bruh")
else:
    for cell in ret:
        print(f"({cell.x}, {cell.y})")

