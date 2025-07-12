import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from time import sleep
from api import *

api = GameClient(7749, "ef80319c")

for spell in SpellType:
  api.cast_spell(spell, Vector2(3, 3))
  if (spell == SpellType.DOUBLE_INCOME and api.get_income(True) != 20):
    api.send_chat(f"[Spell] Money not doubled!")
  sleep(5)

for spell in SpellType:
  api.send_chat(f"Spell {spell} cooldown {int(api.get_spell_cooldown(True, spell))}")
