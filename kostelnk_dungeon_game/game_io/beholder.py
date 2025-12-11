"""
Beholder enemy AI module.

Features:
- Visual: Blue "B" symbol.
- Movement: Moves 2 tiles per hero turn.
- AI: Uses BFS to avoid walls.
- Combat:
    - Melee Attack: Bites if adjacent (dist == 1).
    - Ranged Attack: Casts Firebolt if within 5 tiles and has Line of Sight.
    - Chases hero if within 10 tiles.
    - Wanders randomly if player is far away.
"""

import random
from collections import deque

# ANSI color codes
BLUE = "\033[94m"
RESET = "\033[0m"


class Beholder:
    def __init__(self, x: int, y: int, level: int = 1):
        """
        Initializes the Beholder enemy.
        """
        self.x = x
        self.y = y
        self.level = level

        # --- HP Scaling ---
        base_hp = 100
        hp_per_level = 50
        self.max_hp = base_hp + ((level - 1) * hp_per_level)
        self.hp = self.max_hp

        # Attack power scaling
        # Uložíme sílu útoku do proměnné, kterou používáme v update()
        self.attack_power = 10 + (level * 5)

    def take_damage(self, damage: int, hero_weapon=None, hero_shield=None) -> int:
        """
        Processes damage taken from the Hero with Level 3 immunity check.
        """
        actual_damage = damage

        # --- Level 3 Mechanic: Weapon/Shield Immunity ---
        if self.level >= 3:
            if hero_weapon is None and hero_shield is None:
                # Attack bounces off
                return 0

        self.hp -= actual_damage
        return actual_damage

    def is_alive(self) -> bool:
        """Checks if the Beholder is still alive."""
        return self.hp > 0

    # ----------------------------
    # Helper Methods (Added to fix errors)
    # ----------------------------

    def manhattan_distance(self, tx: int, ty: int) -> int:
        """Calculates distance between self and target (tx, ty)."""
        return abs(self.x - tx) + abs(self.y - ty)

    def is_walkable(self, x: int, y: int, dungeon_map: list[list[str]]) -> bool:
        """Checks if a tile is within bounds and not a wall."""
        if 0 <= y < len(dungeon_map) and 0 <= x < len(dungeon_map[0]):
            return dungeon_map[y][x] != "▓"
        return False

    # ----------------------------
    # Line of Sight & Combat
    # ----------------------------

    def has_line_of_sight(