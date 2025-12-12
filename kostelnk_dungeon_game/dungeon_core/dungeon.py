"""
Dungeon generation module using Random Noise.
"""
import random
from collections import deque
from kostelnk_dungeon_game.dungeon_core.finds import Weapon, Shield, Potion, Gold


class Dungeon:
    """
    Represents the dungeon map, handling generation, layout, and item placement.
    """
    def __init__(self, size: tuple[int, int], level: int = 1):
        """
        Initialize the Dungeon.
        Args:
            size (tuple[int, int]): Dimensions of the dungeon (width, height).
            level (int): Current difficulty level (affects item spawning).
        """
        self.size = size
        self.level = level
        self.dungeon_map = []
        self.items = {}
        self.stairs_pos = None
        self.floor_tiles = []  # List of valid, REACHABLE floor coordinates

    def _generate_noise_map(self, width, height):
        """Generates the initial map using random noise."""
        self.dungeon_map = []
        for y in range(height):
            row = []
            for x in range(width):
                # Borders are always walls
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    row.append("▓")
                else:
                    # 20% chance of a wall
                    if random.random() < 0.2:
                        row.append("▓")
                    else:
                        row.append(".")
            self.dungeon_map.append(row)

    def _clear_start_area(self, width, height):
        """Ensures the starting area (1,1) and neighbors are clear."""
        if width > 1 and height > 1:
            self.dungeon_map[1][1] = "."
            # Clear neighbors to ensure immediate movement
            if width > 2:
                self.dungeon_map[1][2] = "."
            if height > 2:
                self.dungeon_map[2][1] = "."

    def _get_reachable_tiles(self, width, height):
        """Performs BFS to find all reachable tiles from (1,1)."""
        reachable = set()
        queue = deque([(1, 1)])
        visited = {(1, 1)}

        while queue:
            cx, cy = queue.popleft()
            reachable.add((cx, cy))

            # Check 4 directions
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                # Check bounds
                if 0 <= ny < height and 0 <= nx < width:
                    # If it's a floor and not visited
                    if self.dungeon_map[ny][nx] == "." and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        return reachable

    def _place_stairs(self):
        """Places stairs at the furthest reachable point."""
        best_stairs_cand = None
        max_dist = -1

        for (tx, ty) in self.floor_tiles:
            dist = tx + ty  # Simple distance metric from (1,1)
            if dist > max_dist:
                max_dist = dist
                best_stairs_cand = (tx, ty)

        if best_stairs_cand:
            sx, sy = best_stairs_cand
            self.dungeon_map[sy][sx] = ">"
            self.stairs_pos = (sx, sy)
            self.floor_tiles.remove((sx, sy))

    def create_dungeon(self):
        """
        Generates a map using random noise and ensures connectivity using Flood Fill.
        """
        width, height = self.size
        self.items = {}
        self.floor_tiles = []

        # 1. Map Generation
        self._generate_noise_map(width, height)

        # 2. Enforce Start Position
        self._clear_start_area(width, height)

        # 3. Ensure Connectivity (Flood Fill)
        reachable = self._get_reachable_tiles(width, height)

        # If the map is too small (bad generation), regenerate!
        if len(reachable) < 10:
            return self.create_dungeon()

        # 4. Clean up unreachable areas
        for y in range(height):
            for x in range(width):
                if self.dungeon_map[y][x] == "." and (x, y) not in reachable:
                    self.dungeon_map[y][x] = "▓"

        # 5. Populate valid floor tiles list
        self.floor_tiles = list(reachable)

        # Remove (1, 1) from potential item spawn locations (player starts here)
        if (1, 1) in self.floor_tiles:
            self.floor_tiles.remove((1, 1))

        # 6. Place Stairs
        self._place_stairs()

        # 7. Generate Items and Gold
        self._generate_items()
        return None

    def _generate_items(self):
        """
        Spawns weapons, shields, potions, and gold on valid floor tiles.
        """
        if self.level == 1:
            item_count = 1
        elif self.level == 2:
            item_count = 2
        else:
            item_count = 3

        possible_items = [
            Weapon("Iron Sword", attack_bonus=3, weight=4),
            Shield("Wooden Shield", defense_bonus=2, weight=3),
            Potion("Health Potion", effect_type="hp"),
            Potion("Stamina Potion", effect_type="stamina")
        ]

        # Spawn Equipment/Potions
        for _ in range(item_count):
            if not self.floor_tiles:
                break
            ix, iy = random.choice(self.floor_tiles)

            if (ix, iy) not in self.items:
                tmpl = random.choice(possible_items)
                if isinstance(tmpl, Weapon):
                    item = Weapon(tmpl.name, tmpl.attack_bonus, tmpl.weight)
                elif isinstance(tmpl, Shield):
                    item = Shield(tmpl.name, tmpl.defense_bonus, tmpl.weight)
                else:
                    item = Potion(tmpl.name, tmpl.effect_type)

                self.items[(ix, iy)] = item
                self.floor_tiles.remove((ix, iy))

        # Spawn Gold
        for _ in range(random.randint(1, 3)):
            if not self.floor_tiles:
                break
            ix, iy = random.choice(self.floor_tiles)

            if (ix, iy) not in self.items:
                self.items[(ix, iy)] = Gold(random.randint(10, 50))
                self.floor_tiles.remove((ix, iy))

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Checks if a tile is walkable.
        """
        if not (0 <= y < len(self.dungeon_map) and 0 <= x < len(self.dungeon_map[0])):
            return False
        return self.dungeon_map[y][x] != "▓"

    def get_item_at(self, x: int, y: int):
        """
        Retrieves and removes an item from the map at the given coordinates.
        Returns None if no item is present.
        """
        if (x, y) in self.items:
            return self.items.pop((x, y))
        return None

    @staticmethod
    def get_valid_start_position():
        """
        Returns (1, 1) as requested for all levels.
        """
        return 1, 1
