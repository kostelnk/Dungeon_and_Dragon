"""
Beholder enemy AI module.

Features:
- Visual: Blue "B" symbol.
- Movement: Moves 2 tiles per hero turn.
- AI: Uses BFS to avoid walls.
- Combat:
    - Melee Attack: Bites if adjacent.
    - Ranged Attack: Firebolt if visible.
"""

import random
from collections import deque

# ANSI color codes
BLUE = "\033[94m"
RESET = "\033[0m"


class Beholder:
    """
    Represents the Beholder monster.
    """

    def __init__(self, x: int, y: int, level: int = 1):
        """
        Initialize Beholder stats and position.
        Args:
            x, y: Position
            level: Dungeon level (scales HP and Damage)
        """
        self.x = x
        self.y = y
        self.level = level

        # --- HP & Damage Scaling ---
        self.max_hp = 30 + ((level - 1) * 30)
        self.hp = self.max_hp
        self.damage = 5 + ((level - 1) * 3)


        self.name = "Beholder"
        self.symbol = f"{BLUE}B{RESET}"

    # ----------------------------
    # HP Management Logic
    # ----------------------------

    def take_damage(self, amount: int, hero_weapon=None, hero_shield=None) -> int:
        """
        Reduce HP by amount. Returns actual damage dealt.
        """
        # Level 5 no attack without weapon is making damage
        if self.level >= 5:
            if hero_weapon is None and hero_shield is None:
                return 0

        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

        return amount

    def heal(self, amount: int):
        """Increase HP, not exceeding max_hp."""
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def is_alive(self) -> bool:
        """Check if monster is alive."""
        return self.hp > 0

    # ----------------------------
    # Utilities
    # ----------------------------

    def manhattan_distance(self, x2: int, y2: int) -> int:
        """Calculate Manhattan distance to target (x2, y2)."""
        return abs(self.x - x2) + abs(self.y - y2)

    @staticmethod
    def is_walkable(x: int, y: int, dungeon_map: list[list[str]]) -> bool:
        """
        Check if a tile is valid for movement.
        """
        # 1. Kontrola hranic mapy
        if not (0 <= y < len(dungeon_map) and 0 <= x < len(dungeon_map[0])):
            return False

        # 2. Kontrola zdi (pokud to NENÍ zeď, je to průchozí)
        return dungeon_map[y][x] != "▓"

    # ----------------------------
    # Line of Sight & Combat
    # ----------------------------

    def has_line_of_sight(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]) -> bool:
        """Check if there is a clear straight line to the hero."""
        if self.x == hero_x:  # Vertical
            step = 1 if hero_y > self.y else -1
            for y in range(self.y + step, hero_y, step):
                if dungeon_map[y][self.x] == "▓":
                    return False
            return True

        if self.y == hero_y:  # Horizontal
            step = 1 if hero_x > self.x else -1
            for x in range(self.x + step, hero_x, step):
                if dungeon_map[self.y][x] == "▓":
                    return False
            return True

        return False

    def try_firebolt(self, hero) -> bool:
        """Check conditions for Firebolt attack."""
        return self.manhattan_distance(hero.x, hero.y) <= 5

    # ----------------------------
    # Pathfinding (BFS)
    # ----------------------------

    def bfs_next_step(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]):
        """Find the next step towards the hero using BFS."""
        queue = deque([(self.x, self.y)])
        visited = {(self.x, self.y)}
        parent = {}

        target_found = False

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == (hero_x, hero_y):
                target_found = True
                break

            # Zkoušíme 4 směry
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy

                # Používáme opravenou metodu is_walkable
                if (nx, ny) not in visited and self.is_walkable(nx, ny, dungeon_map):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

        if not target_found:
            return None

        # Backtrack
        curr = (hero_x, hero_y)
        max_steps = 100
        steps = 0

        while parent.get(curr) != (self.x, self.y):
            curr = parent.get(curr)
            steps += 1
            if curr is None or steps > max_steps: return None

        return curr

    # ----------------------------
    # Movement Logic
    # ----------------------------

    def move_towards(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]):
        """Executes one step towards the hero."""
        step = self.bfs_next_step(hero_x, hero_y, dungeon_map)

        if step and step != (hero_x, hero_y):
            self.x, self.y = step

    def move_random(self, dungeon_map: list[list[str]], hero_x: int, hero_y: int):
        """Executes one random valid step."""
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = self.x + dx, self.y + dy
            if self.is_walkable(nx, ny, dungeon_map) and (nx, ny) != (hero_x, hero_y):
                self.x, self.y = nx, ny
                return

    def update(self, hero, dungeon_map: list[list[str]]):
        """
        Main AI Loop.
        """
        if not self.is_alive(): return

        dist = self.manhattan_distance(hero.x, hero.y)

        # 1. Melee Attack
        if dist == 1:
            dmg = max(0, self.damage - getattr(hero, 'defense', 0))
            hero.hp -= dmg
            print(f"{BLUE}Beholder bites you for {dmg} damage!{RESET}")
            return

        # 2. Ranged Attack
        if self.try_firebolt(hero) and self.has_line_of_sight(hero.x, hero.y, dungeon_map):
            dmg = random.randint(1, 6) + (self.level * 2)
            hero.hp -= dmg
            print(f"{BLUE}Beholder casts Firebolt! You take {dmg} damage.{RESET}")
            if dist > 2:
                self.move_towards(hero.x, hero.y, dungeon_map)
            return

        # 3. Movement
        steps = 2
        for _ in range(steps):
            dist = self.manhattan_distance(hero.x, hero.y)
            if dist < 10:
                step = self.bfs_next_step(hero.x, hero.y, dungeon_map)
                if step and step != (hero.x, hero.y):
                    self.x, self.y = step
            else:
                self.move_random(dungeon_map, hero.x, hero.y)