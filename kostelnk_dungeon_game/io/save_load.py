"""
Saving and loading game state.
"""

import json


def save_game(hero, beholder, dungeon, path="savefile.json"):
    """
    Save positions and hero stats to a JSON file.
    """
    data = {
        "hero": {"x": hero.x, "y": hero.y, "hp": hero.hp, "gold": hero.gold},
        "beholder": {"x": beholder.x, "y": beholder.y},
        "dungeon": dungeon.dungeon_map,
    }

    with open(path, "w") as f:
        json.dump(data, f)


def load_game(hero, beholder, dungeon, path="savefile.json"):
    """
    Load saved game state from JSON file.
    """
    with open(path, "r") as f:
        data = json.load(f)

    hero.x = data["hero"]["x"]
    hero.y = data["hero"]["y"]
    hero.hp = data["hero"]["hp"]
    hero.gold = data["hero"]["gold"]

    beholder.x = data["beholder"]["x"]
    beholder.y = data["beholder"]["y"]

    dungeon.dungeon_map = data["dungeon"]
