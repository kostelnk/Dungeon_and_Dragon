"""
Main game loop module.
Handles input, rendering, and core game logic flow.
"""

import sys
from kostelnk_dungeon_game.game_io.save_load import save_game, load_game
from kostelnk_dungeon_game.dungeon_core.dungeon import Dungeon
from kostelnk_dungeon_game.dungeon_core.beholder import Beholder
from kostelnk_dungeon_game.dungeon_core.finds import Gold

# ANSI colors
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class GameSession:
    """
    Encapsulates the game state and main loop logic to reduce complexity.
    """
    def __init__(self, dungeon, hero, beholder, renderer):
        self.dungeon = dungeon
        self.hero = hero
        self.beholder = beholder
        self.renderer = renderer
        self.message = "Welcome! Press WASD to move, R to Rest, G to Regen map."
        self.floors_history = {}
        self.moves_on_floor = 0
        self.action_taken = False

    def handle_save_quit(self):
        """Handles saving and quitting the game."""
        confirm = input("Save before quit? (Y/N): ").lower().strip()
        if confirm == 'y':
            save_game(self.hero, self.beholder, self.dungeon)
            print("Game saved successfully.")
        print("Goodbye!")
        sys.exit()

    def handle_regenerate(self):
        """Handles map regeneration command 'G'."""
        if not (self.hero.x == 1 and self.hero.y == 1):
            self.message = (f"{RED}You can only regenerate from "
                            f"the starting position!{RESET}")
            return

        if self.moves_on_floor > 0:
            self.message = (f"{RED}The flux is unstable! "
                            f"You cannot regenerate after exploring.{RESET}")
            return

        self.dungeon.create_dungeon()
        self.beholder.spawn_at_safe_location(
            self.dungeon.floor_tiles, self.hero.x, self.hero.y
        )
        self.message = (f"{GREEN}Flux energy rewrites the reality! "
                        f"Map regenerated.{RESET}")

    def handle_stairs(self):
        """Handles logic when player steps on stairs (>)."""
        # Save current floor state
        self.floors_history[self.dungeon.level] = (self.dungeon, self.beholder)

        # Auto-save progress
        save_game(self.hero, self.beholder, self.dungeon)
        print(f"{GREEN}Progress saved.{RESET}")

        next_level = self.dungeon.level + 1

        if next_level in self.floors_history:
            # Load existing floor
            self.dungeon, self.beholder = self.floors_history[next_level]
            self.hero.x, self.hero.y = 1, 1
            self.message = f"Returned to floor {next_level}."
        else:
            # Generate new floor
            self.dungeon = Dungeon(self.dungeon.size, level=next_level)
            self.dungeon.create_dungeon()

            # Create new Beholder
            self.beholder = Beholder(0, 0, level=next_level)
            self.hero.x, self.hero.y = 1, 1
            self.beholder.spawn_at_safe_location(
                self.dungeon.floor_tiles, self.hero.x, self.hero.y
            )
            self.message = f"Descended to floor {next_level}."

        self.moves_on_floor = 0

    def handle_combat(self, damage):
        """Handles combat interaction with the Beholder."""
        # Apply damage with immunity check
        real_damage = self.beholder.take_damage(
            damage,
            getattr(self.hero, 'weapon', None),
            getattr(self.hero, 'shield', None)
        )

        if real_damage > 0:
            self.message = f"You hit Beholder for {real_damage} dmg!"
        else:
            self.message = (f"{RED}Your attack bounced off! "
                            f"(You need a weapon/shield!){RESET}")

        if self.beholder.hp <= 0:
            self.message += f" {RED} YOU KILLED THE BEHOLDER! {RESET}"

        self.hero.stamina = max(0, self.hero.stamina - 2)
        self.action_taken = True

    def handle_item_pickup(self):
        """Handles picking up items from the ground."""
        item = self.dungeon.get_item_at(self.hero.x, self.hero.y)
        if item:
            if isinstance(item, Gold):
                self.hero.gold += item.amount
                self.message = f"{YELLOW}You found {item.amount} Gold!{RESET}"
            else:
                success = self.hero.add_item(item)
                if success:
                    self.message = f"{CYAN}Picked up {item.name}!{RESET}"
                else:
                    self.dungeon.items[(self.hero.x, self.hero.y)] = item
                    self.message = f"{RED}Inventory full!{RESET}"

    def handle_movement(self, dx, dy):
        """Handles player movement, combat, and environment interaction."""
        target_x = self.hero.x + dx
        target_y = self.hero.y + dy

        # Combat Logic
        if (self.beholder.hp > 0 and
                (target_x, target_y) == (self.beholder.x, self.beholder.y)):
            damage = getattr(self.hero, 'attack_power', 5)
            self.handle_combat(damage)
            return

        # Movement Logic
        moved = self.hero.move(dx, dy, self.dungeon)
        if moved:
            self.action_taken = True
            self.handle_item_pickup()

            # Stairs Logic
            if self.dungeon.dungeon_map[self.hero.y][self.hero.x] == ">":
                self.handle_stairs()

    def process_command(self, cmd, cmd_raw):
        """
        Processes the parsed user command.
        Returns False if the game loop should continue, True otherwise.
        """
        if cmd == 'q':
            self.handle_save_quit()
        elif cmd == 'save':
            save_game(self.hero, self.beholder, self.dungeon)
            self.message = "Game saved manually."
        elif cmd == 'load':
            load_game(self.hero, self.beholder, self.dungeon)
            self.floors_history = {}
            self.moves_on_floor = 0
            self.message = "Game loaded."
        elif cmd == 'r':
            self.hero.rest()
            self.message = "You took a rest to recover stamina."
            self.action_taken = True
        elif cmd == 'g':
            self.handle_regenerate()
        elif cmd == 'i':
            print("\n=== INVENTORY ===")
            print(f"Load: {self.hero.current_load} / Stamina: {self.hero.stamina}")
            print(f"Gold: {self.hero.gold}")
            print(f"Items: {len(self.hero.inventory)}/3")
            for item in self.hero.inventory:
                status = "[E]" if item.equipped else "   "
                print(f"{status} {item.name} (Wt: {item.weight})")
            input("Press Enter...")
        elif cmd == 'e':
            if len(cmd_raw) < 2:
                self.message = "Usage: e <item_name>"
            else:
                target_name = " ".join(cmd_raw[1:])
                self.message = self.hero.use_or_equip(target_name)
                self.action_taken = True
        elif cmd == 'x':
            if len(cmd_raw) < 2:
                self.message = "Usage: x <item_name>"
            else:
                target_name = " ".join(cmd_raw[1:])
                dropped_item = self.hero.drop_item(target_name)
                if not dropped_item:
                    self.message = "Item not found in inventory."
                else:
                    self.dungeon.items[(self.hero.x, self.hero.y)] = dropped_item
                    self.message = f"You dropped {dropped_item.name}."
        elif cmd in ['w', 'a', 's', 'd']:
            current_cost = 1 + self.hero.current_load
            if self.hero.stamina < current_cost:
                self.message = (f"{RED}Too heavy/tired! Cost: {current_cost}, "
                                f"Stamina: {self.hero.stamina}. (Press 'R'){RESET}")
            else:
                dx, dy = 0, 0
                if cmd == 'w':
                    dy = -1
                elif cmd == 's':
                    dy = 1
                elif cmd == 'a':
                    dx = -1
                elif cmd == 'd':
                    dx = 1
                self.handle_movement(dx, dy)
        else:
            self.message = "Unknown command."

    def check_exhaustion(self):
        """Checks if hero is overburdened and drops items if necessary."""
        if self.hero.stamina < self.hero.current_load:
            dropped_msg = []
            for item in self.hero.inventory[:]:
                if item.equipped:
                    item.equipped = False
                    self.hero.inventory.remove(item)
                    self.dungeon.items[(self.hero.x, self.hero.y)] = item
                    dropped_msg.append(item.name)

            if dropped_msg:
                names = ", ".join(dropped_msg)
                self.message += (f" {RED}Collapsed from weight! "
                                 f"Dropped: {names}!{RESET}")

    def enemy_turn(self):
        """Executes the enemy AI turn."""
        if self.action_taken and self.beholder.hp > 0:
            self.moves_on_floor += 1
            self.beholder.update(self.hero, self.dungeon.dungeon_map)

            if self.hero.hp <= 0:
                self.renderer.render(
                    self.dungeon, self.hero, self.beholder, f"{RED}YOU DIED!{RESET}"
                )
                return True  # Game Over
        return False

    def run(self):
        """Runs the main loop."""
        while True:
            self.renderer.render(
                self.dungeon, self.hero, self.beholder, self.message
            )
            self.message = ""
            self.action_taken = False

            cmd_raw = input("Action: ").lower().split()
            if not cmd_raw:
                continue

            self.process_command(cmd_raw[0], cmd_raw)
            self.check_exhaustion()
            if self.enemy_turn():
                break


def game_loop(dungeon, hero, beholder, renderer):
    """
    Entry point for the game loop.
    Creates a GameSession and runs it.
    """
    session = GameSession(dungeon, hero, beholder, renderer)
    session.run()
