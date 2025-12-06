"""
Dungeon generation module.

Contains the Dungeon class responsible for creating and storing the
dungeon map as a 2D grid of tiles.
"""

import random


class Dungeon:
    """
    Represents a single dungeon floor.

    Attributes
    ----------
    size : tuple[int, int]
        Width and height of the dungeon.
    dungeon_map : list[list[str]]
        2D array representing the map.
    """

    def __init__(self, size: tuple[int, int]):
        self.size = size
        self.dungeon_map = []

    def create_dungeon(self):
        """
        Generates a simple dungeon layout with walls and floors.
        '#' is a wall, '.' is a walkable floor.
        """
        width, height = self.size

        self.dungeon_map = []

        for y in range(height):
            row = []
            for x in range(width):
                # Create border walls
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    row.append("▓")
                else:
                    # Random floors and walls
                    row.append("." if random.random() > 0.2 else "▓")
            self.dungeon_map.append(row)

    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if tile at (x, y) is not a wall."""
        return self.dungeon_map[y][x] != "▓"
