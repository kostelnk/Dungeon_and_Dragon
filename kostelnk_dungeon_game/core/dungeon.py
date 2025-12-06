"""
Dungeon generation module.
Manages the grid, walls, items, and stairs.
"""

import random
from core.items import Weapon, Shield, Potion

class Dungeon:
    """
    Represents a single dungeon floor.
    """

    def __init__(self, size: tuple[int, int], level: int = 1):
        self.size = size
        self.level = level
        self.dungeon_map = []
        self.items = {}  # Dictionary {(x, y): Item object}
        self.stairs_pos = None

    def create_dungeon(self):
        """
        Generates map with walls ('▓'), floors ('.'), items, and stairs ('>').
        """
        width, height = self.size
        self.dungeon_map = []
        self.items = {}

        # 1. Build Grid
        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    row.append("▓")
                else:
                    # 20% chance for a wall
                    row.append("." if random.random() > 0.2 else "▓")
            self.dungeon_map.append(row)

        # 2. Place Stairs (ensure reachable in real algo, random for now)
        while True:
            sx, sy = random.randint(1, width-2), random.randint(1, height-2)
            if self.dungeon_map[sy][sx] == ".":
                self.dungeon_map[sy][sx] = ">"
                self.stairs_pos = (sx, sy)
                break

        # 3. Place Items (Randomly)
        possible_items = [
            Weapon("Iron Sword", attack_bonus=3),
            Shield("Wooden Shield", defense_bonus=2),
            Potion("Health Potion", effect_type="hp"),
            Potion("Speed Potion", effect_type="speed")
        ]

        for _ in range(3): # Spawn 3 items per floor
            while True:
                ix, iy = random.randint(1, width-2), random.randint(1, height-2)
                if self.dungeon_map[iy][ix] == ".":
                    item = random.choice(possible_items)
                    self.items[(ix, iy)] = item
                    # Mark on map for rendering logic (optional, renderer handles it via dict)
                    break

    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if tile is not a wall."""
        if not (0 <= y < len(self.dungeon_map) and 0 <= x < len(self.dungeon_map[0])):
            return False
        return self.dungeon_map[y][x] != "▓"

    def get_item_at(self, x: int, y: int):
        """Returns and removes item at position, or None."""
        if (x, y) in self.items:
            return self.items.pop((x, y))
        return None
