"""
Item definitions for the dungeon game.
"""

class Item:
    """Base class for all items."""
    def __init__(self, name: str, item_type: str, weight: int = 0):
        self.name = name
        self.type = item_type
        self.weight = weight # Nový atribut: Váha (stamina cost)
        self.equipped = False

        # Default bonuses
        self.attack_bonus = 0
        self.defense_bonus = 0

    def __repr__(self):
        return f"[{self.name} ({self.type})]"

class Gold(Item):
    """Currency item."""
    def __init__(self, amount: int):
        super().__init__(f"{amount} Gold Coins", "gold", weight=0)
        self.amount = amount

class Weapon(Item):
    """Weapon increasing hero attack."""
    def __init__(self, name: str, attack_bonus: int, weight: int = 3):
        super().__init__(name, "weapon", weight)
        self.attack_bonus = attack_bonus

class Shield(Item):
    """Shield increasing the hero's armor class."""
    def __init__(self, name: str, defense_bonus: int, weight: int = 2):
        super().__init__(name, "shield", weight)
        self.defense_bonus = defense_bonus

class Potion(Item):
    """A potion that applies effects when consumed."""
    def __init__(self, name: str, effect_type: str):
        super().__init__(name, "potion", weight=1) # I lektvar něco váží
        self.effect_type = effect_type

    def apply(self, hero):
        if self.effect_type == "hp":
            hero.hp = min(hero.max_hp, hero.hp + 20)
            print("You drink a health potion and restore 20 HP!")
            return True
        elif self.effect_type == "stamina":
            hero.stamina = min(hero.max_stamina, hero.stamina + 30)
            print("You drink a stamina potion and feel refreshed! (+30 Stamina)")
            return True
        return False