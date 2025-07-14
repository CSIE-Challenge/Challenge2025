import api_importer as api
from test_token import TOKEN1

agent = api.GameClient(7749, TOKEN1)


def print_spell_info(type):
    cd = agent.get_spell_cooldown(True, type)
    print(f"spell type {type.name} -- CD {cd} seconds")


def print_spells():
    print_spell_info(api.SpellType.POISON)
    print_spell_info(api.SpellType.DOUBLE_INCOME)
    print_spell_info(api.SpellType.TELEPORT)


print_spells()

print(
    f"Casting POISON spell {agent.cast_spell(api.SpellType.POISON, api.Vector2(4, 14))}"
)
input("Enter to continue")
print(f"Casting DOUBLE_INCOME spell {agent.cast_spell(api.SpellType.DOUBLE_INCOME)}")
input("Enter to continue")
print(
    f"Casting TELEPORT spell {agent.cast_spell(api.SpellType.TELEPORT, api.Vector2(4, 4))}"
)
input("Enter to continue")

print_spells()

print(
    f"Casting POISON spell {agent.cast_spell(api.SpellType.POISON, api.Vector2(4, 14))}"
)
input("Enter to continue")
print(f"Casting DOUBLE_INCOME spell {agent.cast_spell(api.SpellType.DOUBLE_INCOME)}")
input("Enter to continue")
print(
    f"Casting TELEPORT spell {agent.cast_spell(api.SpellType.TELEPORT, api.Vector2(4, 4))}"
)
input("Enter to continue")
