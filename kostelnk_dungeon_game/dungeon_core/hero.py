"""
Enhanced Hero entity module.
"""

from kostelnk_dungeon_game.dungeon_core.finds import Item

class Hero:
    """
    Represents the player-controlled hero.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hp = 100
        self.max_hp = 100
        self.gold = 0
        self.stamina = 50
        self.max_stamina = 50

        # Base stats
        self.base_attack = 5
        self.base_defense = 0

        # Inventory list
        self.inventory: list[Item] = []

    @property
    def attack(self) -> int:
        return self.base_attack + sum(i.attack_bonus for i in self.inventory if i.equipped)

    @property
    def defense(self) -> int:
        return self.base_defense + sum(i.defense_bonus for i in self.inventory if i.equipped)

    @property
    def current_load(self) -> int:
        """Calculates total weight of EQUIPPED items."""
        return sum(i.weight for i in self.inventory if i.equipped)

    def add_item(self, item: Item) -> bool:
        """
        Adds an item to the inventory if space allows (Max 3 items).
        Returns True if successful, False if inventory is full.
        """
        if len(self.inventory) >= 3:
            return False

        self.inventory.append(item)
        return True

    def drop_item(self, item_name: str):  # Return type: Item or None
        """
        Removes an item from inventory by name and returns it.
        Used when the player wants to drop something on the ground.
        """
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                item.equipped = False  # Ensure it is not equipped
                return self.inventory.pop(i)
        return None

    def rest(self):
        """Restores stamina."""
        amount = 15
        self.stamina = min(self.max_stamina, self.stamina + amount)
        print(f"You rest for a while. Stamina +{amount}.")

    def use_or_equip(self, item_name: str) -> str:
        """
        Universal method for item interaction.
        Potions are removed after use.
        """
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                # A) Potion -> Use (Consume)
                if item.type == "potion":
                    # --- NOVÁ MECHANIKA: Cena za použití lektvaru ---
                    cost = item.weight
                    if self.stamina < cost:
                        return f"Too exhausted to use {item.name}! (Needs {cost} Stamina)"

                    self.stamina -= cost
                    used = item.apply(self)

                    if used:
                        self.inventory.pop(i)
                        return f"You drank {item.name} (Stamina cost: {cost})."
                    return f"Could not use {item.name}."

                # B) Equipment -> Toggle Equip
                else:
                    item.equipped = not item.equipped
                    status = "equipped" if item.equipped else "unequipped"
                    return f"You {status} {item.name}."

        return "Item not found in inventory."

    def move(self, dx: int, dy: int, dungeon):
        """
        Moves hero. Returns True if move happened.
        Now calculates dynamic stamina cost based on load.
        """
        # --- NEW MECHANIC: Cost of movement = 1 + load---
        move_cost = 1 + self.current_load

        if self.stamina < move_cost:
                        return False

        new_x = self.x + dx
        new_y = self.y + dy

        if dungeon.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.stamina -= move_cost
            return True
        return False