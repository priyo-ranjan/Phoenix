import random

from cogs.eggs import roll_rarity
from .creatures import CREATURES

def hatch_creature(egg_type):
    creatures = CREATURES.get(egg_type, [])

    if not creatures:
        return None

    rarity = roll_rarity(egg_type)

    possible_creatures = [
        creature
        for creature in creatures
        if creature["rarity"] == rarity
    ]

    if not possible_creatures:
        return None

    weights = [
        creature["weight"]
        for creature in possible_creatures
    ]

    creature = random.choices(
        possible_creatures,
        weights=weights,
        k=1
    )[0]

    return creature