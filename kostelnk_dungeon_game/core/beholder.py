"""
Beholder enemy AI.

Features:
- Moves 2 tiles per hero turn
- Uses BFS to avoid walls and chase hero intelligently
- Can cast Firebolt (1–6 dmg) if within 5 tiles with clear LoS
"""

import random
from collections import deque


class Beholder:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # ----------------------------
    # Basic utilities
    # ----------------------------

    def manhattan_distance(self, x2: int, y2: int):
        return abs(self.x - x2) + abs(self.y - y2)

    def is_walkable(self, x, y, dungeon_map):
        return (
            0 <= x < len(dungeon_map[0]) and
            0 <= y < len(dungeon_map) and
            dungeon_map[y][x] == "."
        )

    # ----------------------------
    # Line of sight (simple straight-line check)
    # ----------------------------

    def has_line_of_sight(self, hero_x, hero_y, dungeon_map):
        """
        Straight line check — Beholder can only cast Firebolt if hero is
        horizontally or vertically aligned with no wall between them.
        """

        if self.x == hero_x:  # vertical LoS
            step = 1 if hero_y > self.y else -1
            for y in range(self.y + step, hero_y, step):
                if dungeon_map[y][self.x] != ".":
                    return False
            return True

        if self.y == hero_y:  # horizontal LoS
            step = 1 if hero_x > self.x else -1
            for x in range(self.x + step, hero_x, step):
                if dungeon_map[self.y][x] != ".":
                    return False
            return True

        return False  # not aligned → no LoS

    # ----------------------------
    # BFS pathfinding
    # ----------------------------

    def bfs_next_step(self, hero_x, hero_y, dungeon_map):
        """
        Returns next tile (x, y) in shortest path to hero using BFS.
        If no path exists, return None.
        """

        queue = deque()
        queue.append((self.x, self.y))
        visited = {(self.x, self.y)}
        parent = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == (hero_x, hero_y):
                break

            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = x + dx, y + dy

                if (nx, ny) not in visited and self.is_walkable(nx, ny, dungeon_map):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        # If hero not found
        if (hero_x, hero_y) not in visited:
            return None

        # reconstruct path back to start
        step = (hero_x, hero_y)
        while parent.get(step) != (self.x, self.y):
            step = parent[step]

        return step

    # ----------------------------
    # Movement behaviors
    # ----------------------------

    def move_towards(self, hero_x, hero_y, dungeon_map):
        """
        Move one step towards hero using BFS.
        If no path exists, do nothing.
        """
        step = self.bfs_next_step(hero_x, hero_y, dungeon_map)
        if step:
            self.x, self.y = step

    def move_random(self, dungeon_map):
        """
        Move one random step if possible.
        """
        random.shuffle(DIRS := [(1,0), (-1,0), (0,1), (0,-1)])

        for dx, dy in DIRS:
            nx = self.x + dx
            ny = self.y + dy
            if self.is_walkable(nx, ny, dungeon_map):
                self.x = nx
                self.y = ny
                return

    # ----------------------------
    # Combat
    # ----------------------------

    def try_firebolt(self, hero):
        """
        Firebolt:
        - only if aligned horizontally or vertically
        - no walls between
        - max range 5 (Manhattan)
        """
        if self.manhattan_distance(hero.x, hero.y) > 5:
            return False

        return True

    # ----------------------------
    # Main update
    # ----------------------------

    def update(self, hero, dungeon_map):
        """
        Called once after hero moves.

        Behaviour priority:
        1) If Firebolt possible → shoot → move 1 step
        2) Otherwise move 2 steps toward hero
        """

        # --- Attempt FIREBOLT ---
        if self.try_firebolt(hero) and self.has_line_of_sight(hero.x, hero.y, dungeon_map):

            dmg = random.randint(1, 6)
            hero.hp -= dmg
            print(f"🔥 Beholder hits you with Firebolt for {dmg} damage! Your HP: {hero.hp}")

            # After firebolt → move only once
            self.move_towards(hero.x, hero.y, dungeon_map)
            return

        # --- Otherwise: move twice ---
        for _ in range(2):
            step = self.bfs_next_step(hero.x, hero.y, dungeon_map)
            if step:
                self.x, self.y = step
            else:
                self.move_random(dungeon_map)
