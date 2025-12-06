"""
Beholder enemy AI module.

Features:
- Visual: Blue "B" symbol.
- Movement: Moves 2 tiles per hero turn.
- AI: Uses BFS to avoid walls.
- Combat:
    - Casts Firebolt (1-6 dmg) if within 5 tiles and has Line of Sight.
    - Chases hero if within 10 tiles (Manhattan distance).
    - Wanders randomly if player is far away.
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

    def __init__(self, x: int, y: int):
        """
        Initialize Beholder stats and position.

        Parameters
        ----------
        x, y : int
            Initial position.
        """
        self.x = x
        self.y = y
        self.hp = 30
        self.max_hp = 30
        self.damage = 5       # Base melee damage
        self.xp_reward = 100
        self.name = "Beholder"
        self.symbol = f"{BLUE}B{RESET}"

    # ----------------------------
    # Utilities
    # ----------------------------

    def manhattan_distance(self, x2: int, y2: int) -> int:
        """Calculate Manhattan distance to target (x2, y2)."""
        return abs(self.x - x2) + abs(self.y - y2)

    def is_walkable(self, x: int, y: int, dungeon_map: list[list[str]]) -> bool:
        """Check if a tile is valid for movement (within bounds and floor)."""
        return (
            0 <= x < len(dungeon_map[0]) and
            0 <= y < len(dungeon_map) and
            dungeon_map[y][x] in [".", ">", "S", "W", "P"] # Allow stepping on items/stairs
        )

    # ----------------------------
    # Line of Sight & Combat
    # ----------------------------

    def has_line_of_sight(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]) -> bool:
        """
        Check if there is a clear straight line (horizontal/vertical) to the hero.
        Used for Firebolt attacks.
        """
        if self.x == hero_x:  # Vertical
            step = 1 if hero_y > self.y else -1
            for y in range(self.y + step, hero_y, step):
                if dungeon_map[y][self.x] == "▓": # Wall check
                    return False
            return True

        if self.y == hero_y:  # Horizontal
            step = 1 if hero_x > self.x else -1
            for x in range(self.x + step, hero_x, step):
                if dungeon_map[self.y][x] == "▓": # Wall check
                    return False
            return True

        return False

    def try_firebolt(self, hero) -> bool:
        """
        Check conditions for Firebolt attack.
        Requires distance <= 5.
        """
        return self.manhattan_distance(hero.x, hero.y) <= 5

    # ----------------------------
    # Pathfinding (BFS)
    # ----------------------------

    def bfs_next_step(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]):
        """
        Find the next step towards the hero using Breadth-First Search (BFS).
        Guarantees shortest path avoiding obstacles.
        """
        queue = deque([(self.x, self.y)])
        visited = {(self.x, self.y)}
        parent = {}

        target_found = False

        while queue:
            cx, cy = queue.popleft()
            if (cx, cy) == (hero_x, hero_y):
                target_found = True
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in visited and self.is_walkable(nx, ny, dungeon_map):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

        if not target_found:
            return None

        # Backtrack to find the first step
        curr = (hero_x, hero_y)
        while parent.get(curr) != (self.x, self.y):
            curr = parent.get(curr)
            if curr is None: return None # Should not happen if path exists

        return curr

    # ----------------------------
    # AI Logic
    # ----------------------------

    def move_towards(self, hero_x: int, hero_y: int, dungeon_map: list[list[str]]):
        """Executes one step towards the hero."""
        step = self.bfs_next_step(hero_x, hero_y, dungeon_map)
        if step:
            self.x, self.y = step

    def move_random(self, dungeon_map: list[list[str]]):
        """Executes one random valid step."""
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = self.x + dx, self.y + dy
            if self.is_walkable(nx, ny, dungeon_map):
                self.x, self.y = nx, ny
                return

    def update(self, hero, dungeon_map: list[list[str]]):
        """
        Main AI Loop. Called after hero moves.

        Logic:
        1. Firebolt: If dist <= 5 and LoS -> Attack (1-6 dmg) and move 1 step.
        2. Chase: If dist < 10 -> Move 2 steps towards hero intelligently.
        3. Wander: If dist >= 10 -> Move 2 steps randomly.
        """
        dist = self.manhattan_distance(hero.x, hero.y)

        # 1. Ranged Attack
        if self.try_firebolt(hero) and self.has_line_of_sight(hero.x, hero.y, dungeon_map):
            dmg = random.randint(1, 6)
            hero.hp -= dmg
            print(f"{BLUE}Beholder casts Firebolt! You take {dmg} damage.{RESET}")

            # Action cost: Attack takes time, so only move 1 step
            self.move_towards(hero.x, hero.y, dungeon_map)
            return

        # Movement points (speed)
        steps = 2

        # 2. Chase or Wander
        for _ in range(steps):
            # Recalculate distance for dynamic updates between steps
            dist = self.manhattan_distance(hero.x, hero.y)

            if dist < 10:
                # Intelligent chase
                self.move_towards(hero.x, hero.y, dungeon_map)
            else:
                # Idle wandering
                self.move_random(dungeon_map)
