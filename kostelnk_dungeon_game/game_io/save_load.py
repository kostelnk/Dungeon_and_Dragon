"""
Saving and loading game state.
"""

import json
from kostelnk_dungeon_game.dungeon_core.finds import Weapon, Shield, Potion, Gold

def serialize_item(item):
    """Help function: Changes Item for dictionary for JSON."""
    data = {
        "class": item.__class__.__name__,
        "name": item.name,
        "type": item.type,
        "weight": item.weight,
        "equipped": getattr(item, "equipped", False)
    }

    # Specific attributes
    if isinstance(item, Weapon):
        data["attack_bonus"] = item.attack_bonus
    elif isinstance(item, Shield):
        data["defense_bonus"] = item.defense_bonus
    elif isinstance(item, Potion):
        data["effect_type"] = item.effect_type
    elif isinstance(item, Gold):
        data["amount"] = item.amount

    return data

def deserialize_item(data):
    """Help function: Makes Item from dictionary."""
    cls_name = data.get("class")

    if cls_name == "Weapon":
        item = Weapon(data["name"], data["attack_bonus"], data["weight"])
    elif cls_name == "Shield":
        item = Shield(data["name"], data["defense_bonus"], data["weight"])
    elif cls_name == "Potion":
        item = Potion(data["name"], data["effect_type"])
    elif cls_name == "Gold":
        item = Gold(data["amount"])
    else:
        return None # Unknown object

    # Restoring equipment status
    if data.get("equipped", False):
        item.equipped = True

    return item

def save_game(hero, beholder, dungeon, path="savefile.json"):
    """
    Save complete game state to a JSON file.
    """
    # 1. Inventory save
    inventory_data = [serialize_item(item) for item in hero.inventory]

    # 2. Save items on the map
    # Convert the coordinates (x, y) to a list
    map_items_data = []
    for (x, y), item in dungeon.items.items():
        map_items_data.append({
            "x": x,
            "y": y,
            "item": serialize_item(item)
        })

    data = {
        "level": dungeon.level,
        "hero": {
            "x": hero.x,
            "y": hero.y,
            "hp": hero.hp,
            "max_hp": hero.max_hp,
            "stamina": hero.stamina,
            "max_stamina": hero.max_stamina,
            "gold": hero.gold,
            "inventory": inventory_data
        },
        "beholder": {
            "x": beholder.x,
            "y": beholder.y,
            "hp": beholder.hp  # Important for not healing the B
        },
        "dungeon": {
            "map": dungeon.dungeon_map,
            "items": map_items_data,
            "stairs": dungeon.stairs_pos
        }
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4) # indent=4 pro readability


def load_game(hero, beholder, dungeon, path="savefile.json"):
    """
    Load game state from JSON file and reconstruct objects.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Load Dungeon
    dungeon.level = data.get("level", 1)
    dungeon.dungeon_map = data["dungeon"]["map"]
    dungeon.stairs_pos = tuple(data["dungeon"]["stairs"]) if data["dungeon"]["stairs"] else None

    # Restore items on the map
    dungeon.items = {}
    for entry in data["dungeon"]["items"]:
        item_obj = deserialize_item(entry["item"])
        if item_obj:
            dungeon.items[(entry["x"], entry["y"])] = item_obj

    # 2. Load Hero
    h_data = data["hero"]
    hero.x = h_data["x"]
    hero.y = h_data["y"]
    hero.hp = h_data["hp"]
    hero.max_hp = h_data.get("max_hp", 100)
    hero.stamina = h_data.get("stamina", 50)
    hero.max_stamina = h_data.get("max_stamina", 50)
    hero.gold = h_data["gold"]

    # Restore inventory
    hero.inventory = []
    for item_data in h_data["inventory"]:
        item_obj = deserialize_item(item_data)
        if item_obj:
            hero.inventory.append(item_obj)

    # 3. Load Beholder
    b_data = data["beholder"]
    beholder.x = b_data["x"]
    beholder.y = b_data["y"]
    beholder.hp = b_data.get("hp", 30)
    # If HP is missing in the savefile, set the default value of 30.
