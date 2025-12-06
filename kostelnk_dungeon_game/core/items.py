"""
Item definitions for the dungeon game.
This module defines several item types: weapons, shields, potions.
Each item has:
- name
- type (weapon, shield, potion)
- attack_bonus / defense_bonus / effects
- whether the hero has it equipped or not
"""

class Item:
    """Base class for all items."""
    def __init__(self, name: str, item_type: str):
        self.name = name
        self.type = item_type
        self.equipped = False  # hero can own but not equip

    def __repr__(self):
        return f"<Item {self.name} ({self.type})>"


class Weapon(Item):
    """Weapon increasing hero attack."""
    def __init__(self, name: str, attack_bonus: int, stamina_cost: int = 0):
        super().__init__(name, "weapon")
        self.attack_bonus = attack_bonus
        self.stamina_cost = stamina_cost


class Shield(Item):
    """Shield increasing the hero's armor class."""
    def __init__(self, name: str, defense_bonus: int):
        super().__init__(name, "shield")
        self.defense_bonus = defense_bonus


class Potion(Item):
    """A potion that applies effects when consumed."""
    def __init__(self, name: str, effect_type: str):
        super().__init__(name, "potion")
        self.effect_type = effect_type

    def apply(self, hero):
        """
        Apply potion effect:
        - hp_potion: restore HP
        - speed_potion: give 3 steps in 1 turn
        """
        if self.effect_type == "hp":
            hero.hp = min(hero.max_hp, hero.hp + 10)
            print("You drink a health potion and restore 10 HP!")

        elif self.effect_type == "speed":
            hero.speed = 3
            hero.speed_turns = 1
            print("⚡ You feel faster! You will move 3 steps this turn.")

        # potion is consumed
        return True