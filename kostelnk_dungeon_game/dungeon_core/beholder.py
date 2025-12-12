"""
Beholder enemy AI module.
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
    # pylint: disable=too-many-instance-attributes

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
        self.attack_power = 10 + (level * 5)

        self.name = "Beholder"
        self.symbol = f"{BLUE}B{RESET}"

    def spawn_at_safe_location(self, floor_tiles: list[tuple[int, int]],
                               player_x: int, player_y: int):
        """
        Teleports the Beholder to a random floor tile at least 5 steps
        away from the player.
        """
        possible_targets = []

        # Find tiles far away
        for (tx, ty) in floor_tiles:
            dist_x = abs(tx - player_x)
            dist_y = abs(ty - player_y)

            # Check distance
            if dist_x >= 5 or dist_y >= 5:
                possible_targets.append((tx, ty))

        # Pick a spot
        if possible_targets:
            self.x, self.y = random.choice(possible_targets)
        elif floor_tiles:
            self.x, self.y = random.choice(floor_tiles)
        else:
            # Fallback (should rarely happen)
            self.x, self.y = player_x, player_y

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
        self.hp = max(self.hp, 0)
        return actual_damage

    def is_alive(self) -> bool:
        """Checks if the Beholder is still alive."""
        return self.hp > 0

    def manhattan_distance(self, tx: int, ty: int) -> int:
        """Calculates distance between self and target (tx, ty)."""
        return abs(self.x - tx) + abs(self.y - ty)

    @staticmethod
    def is_walkable(x: int, y: int, dungeon_map: list[list[str]]) -> bool:
        """Checks if a tile is within bounds and not a wall."""
        if 0 <= y < len(dungeon_map) and 0 <= x < len(dungeon_map[0]):
            return dungeon_map[y][x] != "▓"
        return False

    def has_line_of_sight(self, hero_x: int, hero_y: int,
                          dungeon_map: list[list[str]]) -> bool:
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

    def _reconstruct_path(self, parent: dict, target_pos: tuple[int, int]):
        """Backtracks from target to find the next step."""
        curr = target_pos
        max_steps = 100
        steps = 0

        while parent.get(curr) != (self.x, self.y):
            curr = parent.get(curr)
            steps += 1
            if curr is None or steps > max_steps:
                return None
        return curr

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

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in visited and self.is_walkable(nx, ny, dungeon_map):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (cx, cy)
                    queue.append((nx, ny))

        if not target_found:
            return None

        return self._reconstruct_path(parent, (hero_x, hero_y))

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
        if not self.is_alive():
            return

        dist = self.manhattan_distance(hero.x, hero.y)

        # 1. Melee Attack
        if dist == 1:
            dmg = max(0, self.attack_power - getattr(hero, 'defense', 0))
            hero.hp -= dmg
            print(f"{BLUE}Beholder bites you for {dmg} damage!{RESET}")
            return

        # 2. Ranged Attack
        if self.try_firebolt(hero) and \
                self.has_line_of_sight(hero.x, hero.y, dungeon_map):
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
