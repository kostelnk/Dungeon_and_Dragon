"""
Enhanced Hero entity module with inventory, equipment, and effective stats.
"""

class Item:
    """
    Represents an item the hero can own.

    Parameters
    ----------
    name : str
        Item name.
    attack_bonus : int
        Bonus added to hero's attack when equipped.
    defense_bonus : int
        Bonus added to hero's defense (AC) when equipped.
    """
    def __init__(self, name: str, attack_bonus: int = 0, defense_bonus: int = 0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.equipped = False


class Hero:
    """
    Represents the player-controlled hero.

    Attributes
    ----------
    x, y : int
        Current hero position in the dungeon map.
    hp : int
        Hit points.
    gold : int
        Gold the hero carries.
    inventory : list[Item]
        All items the hero owns.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 20
        self.gold = 0

        # Base stats
        self.base_attack = 2
        self.base_defense = 0

        # Owned items
        self.inventory: list[Item] = []

    # ----------------------------
    # Effective stats
    # ----------------------------
    @property
    def attack(self) -> int:
        """Total attack including equipped bonuses."""
        return self.base_attack + sum(i.attack_bonus for i in self.inventory if i.equipped)

    @property
    def defense(self) -> int:
        """Total defense including equipped bonuses."""
        return self.base_defense + sum(i.defense_bonus for i in self.inventory if i.equipped)

    # ----------------------------
    # Inventory management
    # ----------------------------
    def add_item(self, item: Item):
        """Add an item to the hero inventory."""
        self.inventory.append(item)
        print(f"You found {item.name}!")

    def equip_item(self, item_name: str):
        """Equip an item by name if owned."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item.equipped = True
                print(f"Equipped {item.name}.")
                return
        print("Item not found.")

    def unequip_item(self, item_name: str):
        """Unequip an owned item."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item.equipped = False
                print(f"Unequipped {item.name}.")
                return
        print("Item not found.")

    # ----------------------------
    # Movement
    # ----------------------------
    def move(self, dx: int, dy: int, dungeon):
        """
        Move hero by (dx, dy) if tile is walkable.
        Returns True if movement succeeds.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        if dungeon.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False
