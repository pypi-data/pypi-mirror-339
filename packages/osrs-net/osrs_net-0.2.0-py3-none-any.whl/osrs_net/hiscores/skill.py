from enum import Enum

skills_list = ['total', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 'cooking', 'woodcutting',
        'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving',
        'slayer', 'farming', 'runecraft', 'hunter', 'construction']


class Skill(Enum):
    TOTAL = 'total'
    ATTACK = 'attack'
    DEFENCE = 'defence'
    STRENGTH = 'strength'
    HITPOINTS = 'hitpoints'
    RANGED = 'ranged'
    PRAYER = 'prayer'
    MAGIC = 'magic'
    COOKING = 'cooking'
    WOODCUTTING = 'woodcutting'
    FLETCHING = 'fletching'
    FISHING = 'fishing'
    FIREMAKING = 'firemaking'
    CRAFTING = 'crafting'
    SMITHING = 'smithing'
    MINING = 'mining'
    HERBLORE = 'herblore'
    AGILITY = 'agility'
    THIEIVNG = 'thieving'
    SLAYER = 'slayer'
    FARMING = 'farming'
    RUNECRAFT = 'runecraft'
    HUNTER = 'hunter'
    CONSTRUCTION = 'construction'


    @classmethod
    def from_string(cls, str_value):
        for member in cls:
            if member.value == str_value.lower():
                return member
        raise ValueError(f"{str_value} is not a valid skill string.")
