from .defs import *
from .game_client import GameClient
from .utils import is_auto_invoked


if is_auto_invoked():
    import os, sys
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
