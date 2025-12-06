"""
Inventory system for the dungeon game.
The hero can carry exactly 2 items.
Items may be equipped (weapon/shield) or consumed (potions).
"""

from core.items import Item, Weapon, Shield, Potion

class Inventory:
    """Represents the hero's inventory with exactly 2 slots."""

    MAX_SLOTS = 2

    def __init__(self):
        self.slots: list[Item | None] = [None, None]

    # ------------------------------------------------------
    # Basic operations
    # ------------------------------------------------------

    def has_space(self) -> bool:
        return any(slot is None for slot in self.slots)

    def add_item(self, item: Item) -> bool:
        """Add item to first empty slot. Returns True if successful."""
        for i in range(self.MAX_SLOTS):
            if self.slots[i] is None:
                self.slots[i] = item
                print(f"Picked up {item.name}!")
                return True
        print("Inventory is full! Cannot pick up item.")
        return False

    def remove_item(self, index: int) -> Item | None:
        """Remove an item from a slot and return it."""
        if 0 <= index < self.MAX_SLOTS:
            item = self.slots[index]
            self.slots[index] = None
            return item
        return None

    # ------------------------------------------------------
    # Equip logic
    # ------------------------------------------------------

    def equip_item(self, index: int, hero) -> bool:
        """
        Equip a weapon or shield.
        Potions cannot be equipped.
        """
        if 0 <= index < self.MAX_SLOTS and self.slots[index]:
            item = self.slots[index]

            if isinstance(item, Weapon):
                hero.weapon = item
                item.equipped = True
                print(f"You equip the weapon: {item.name}.")
                return True

            if isinstance(item, Shield):
                hero.shield = item
                item.equipped = True
                print(f"You equip the shield: {item.name}.")
                return True

            print("Cannot equip this item.")
        return False

    # ------------------------------------------------------
    # Potion usage
    # ------------------------------------------------------

    def use_item(self, index: int, hero) -> bool:
        """Consume a potion if present."""
        if 0 <= index < self.MAX_SLOTS and self.slots[index]:
            item = self.slots[index]

            if isinstance(item, Potion):
                consumed = item.apply(hero)
                if consumed:
                    self.slots[index] = None
                return consumed

            print("You cannot use this item directly.")
            return False

        return False

    # ------------------------------------------------------
    # Display
    # ------------------------------------------------------

    def display(self):
        """Print current inventory contents."""
        print("\nInventory:")
        for i, item in enumerate(self.slots):
            if item:
                eq = " (equipped)" if item.equipped else ""
                print(f" {i+1}. {item.name}{eq}")
            else:
                print(f" {i+1}. [empty]")
        print()