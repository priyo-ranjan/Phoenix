import random

RARITY_CHANCES = {

    "common": {
        "Common": 60.0,
        "Uncommon": 25.0,
        "Rare": 10.0,
        "Very Rare": 5.0,
    },

    "extinct": {
        "Common": 50.0,
        "Uncommon": 25.0,
        "Rare": 15.0,
        "Very Rare": 7.0,
        "Legendary": 2.5,
        "Mythic": 0.5,
    },

    "dragon": {
        "Common": 45.0,
        "Uncommon": 25.0,
        "Rare": 15.0,
        "Very Rare": 9.0,
        "Legendary": 5.0,
        "Mythic": 1.0,
    },

    "mythic": {
        "Common": 35.0,
        "Uncommon": 25.0,
        "Rare": 18.0,
        "Very Rare": 12.0,
        "Legendary": 7.0,
        "Mythic": 3.0,
    },

    "cosmic": {
        "Common": 25.0,
        "Uncommon": 20.0,
        "Rare": 20.0,
        "Very Rare": 15.0,
        "Legendary": 12.0,
        "Mythic": 8.0,
    }
}

def roll_rarity(egg_type):
    """
    Rolls a rarity based on the egg's probability table.
    """

    rarities = RARITY_CHANCES[egg_type]

    rarity = random.choices(
        list(rarities.keys()),
        weights=list(rarities.values()),
        k=1
    )[0]

    return rarity


