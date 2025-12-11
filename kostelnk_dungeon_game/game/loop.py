import sys
import random
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


def respawn_beholder(dungeon, beholder, start_x, start_y):
    """
    Helper function to safely spawn the Beholder far from the start position.

    Args:
        dungeon: The current Dungeon instance.
        beholder: The Beholder instance.
        start_x: Player's X coordinate (to avoid).
        start_y: Player's Y coordinate (to avoid).
    """
    possible_targets = []

    # Look for valid floor tiles far from the player
    for (tx, ty) in dungeon.floor_tiles:
        dist_x = abs(tx - start_x)
        dist_y = abs(ty - start_y)

        if dist_x >= 5 or dist_y >= 5:
            possible_targets.append((tx, ty))

    if possible_targets:
        bx, by = random.choice(possible_targets)
        beholder.x = bx
        beholder.y = by
    else:
        # Fallback for extremely small maps
        beholder.x = 3
        beholder.y = 3


def game_loop(dungeon, hero, beholder, renderer):
    """
    Main game loop handling input, rendering, and game logic.

    Args:
        dungeon: The Dungeon object.
        hero: The Hero object.
        beholder: The Beholder object.
        renderer: The Renderer object.
    """
    message = "Welcome! Press WASD to move, R to Rest, G to Regen map."

    # Stores visited floors to allow returning without regeneration
    floors_history = {}

    # Counter for actions taken on the current floor (prevents map regeneration abuse)
    moves_on_floor = 0

    while True:
        # 1. Render the game state
        renderer.render(dungeon, hero, beholder, message)
        message = ""

        # 2. Get Input
        cmd_raw = input("Action: ").lower().split()
        if not cmd_raw: continue
        cmd = cmd_raw[0]

        dx, dy = 0, 0
        action_taken = False

        # --- COMMAND PROCESSING ---

        if cmd == 'q':
            # Save and Quit
            confirm = input("Save before quit? (Y/N): ").lower().strip()
            if confirm == 'y':
                save_game(hero, beholder, dungeon)
                print("Game saved successfully.")
            print("Goodbye!")
            sys.exit()

        elif cmd == 'save':
            save_game(hero, beholder, dungeon)
            message = "Game saved manually."
            continue

        elif cmd == 'load':
            load_game(hero, beholder, dungeon)
            floors_history = {}  # Reset history on load (simple implementation)
            moves_on_floor = 0  # Reset move counter
            message = "Game loaded."
            continue

        elif cmd == 'r':
            # Rest action
            hero.rest()
            message = "You took a rest to recover stamina."
            action_taken = True

        elif cmd == 'g':
            # Regenerate Map Action
            # Condition 1: Must be at start position
            if not (hero.x == 1 and hero.y == 1):
                message = f"{RED}You can only regenerate from the starting position!{RESET}"
                continue

            # Condition 2: Must not have made any moves on this floor
            if moves_on_floor > 0:
                message = f"{RED}The flux is unstable! You cannot regenerate after exploring.{RESET}"
                continue

            # Execute Regeneration
            dungeon.create_dungeon()
            respawn_beholder(dungeon, beholder, hero.x, hero.y)
            message = f"{GREEN}Flux energy rewrites the reality! Map regenerated.{RESET}"
            continue

        elif cmd == 'i':
            # Show Inventory
            print("\n=== INVENTORY ===")
            print(f"Load: {hero.current_load} / Stamina: {hero.stamina}")
            print(f"Gold: {hero.gold}")
            print(f"Items: {len(hero.inventory)}/3")
            for item in hero.inventory:
                status = "[E]" if item.equipped else "   "
                print(f"{status} {item.name} (Wt: {item.weight})")
            input("Press Enter...")
            continue

        elif cmd == 'e':
            # Equip / Use Item
            if len(cmd_raw) < 2:
                message = "Usage: e <item_name>"
            else:
                target_name = " ".join(cmd_raw[1:])
                message = hero.use_or_equip(target_name)
                # Using an item counts as an action (prevents regen after buffing)
                action_taken = True
            continue

        elif cmd == 'x':
            # Drop Item
            if len(cmd_raw) < 2:
                message = "Usage: x <item_name>"
            else:
                target_name = " ".join(cmd_raw[1:])
                dropped_item = hero.drop_item(target_name)

                if dropped_item:
                    dungeon.items[(hero.x, hero.y)] = dropped_item
                    message = f"You dropped {dropped_item.name}."
                    action_taken = True
                else:
                    message = "Item not found in inventory."
            continue

        elif cmd in ['w', 'a', 's', 'd']:
            # Movement preparation
            current_cost = 1 + hero.current_load
            if hero.stamina < current_cost:
                message = f"{RED}Too heavy/tired! Cost: {current_cost}, Stamina: {hero.stamina}. (Press 'R'){RESET}"
                continue

            if cmd == 'w':
                dy = -1
            elif cmd == 's':
                dy = 1
            elif cmd == 'a':
                dx = -1
            elif cmd == 'd':
                dx = 1

            target_x = hero.x + dx
            target_y = hero.y + dy

            # --- COMBAT LOGIC ---
            if beholder.hp > 0 and (target_x, target_y) == (beholder.x, beholder.y):
                # Retrieve attack power safely
                damage = getattr(hero, 'attack_power', 5)
                # Apply damage with potential Level 3 immunity check
                real_damage = beholder.take_damage(damage, getattr(hero, 'weapon', None), getattr(hero, 'shield', None))

                if real_damage > 0:
                    message = f"You hit Beholder for {real_damage} dmg!"
                else:
                    message = f"{RED}Your attack bounced off! (You need a weapon/shield!){RESET}"

                if beholder.hp <= 0:
                    message += f" {RED} YOU KILLED THE BEHOLDER! {RESET}"

                hero.stamina = max(0, hero.stamina - 2)
                action_taken = True

            # --- MOVEMENT LOGIC ---
            else:
                moved = hero.move(dx, dy, dungeon)
                if moved:
                    action_taken = True

                    # 1. Item Pickup
                    item = dungeon.get_item_at(hero.x, hero.y)
                    if item:
                        if isinstance(item, Gold):
                            hero.gold += item.amount
                            message = f"{YELLOW}You found {item.amount} Gold!{RESET}"
                        else:
                            success = hero.add_item(item)
                            if success:
                                message = f"{CYAN}Picked up {item.name}!{RESET}"
                            else:
                                dungeon.items[(hero.x, hero.y)] = item
                                message = f"{RED}Inventory full!{RESET}"

                    # 2. Stairs Logic (Level Transition)
                    if dungeon.dungeon_map[hero.y][hero.x] == ">":
                        # Save current floor state to history
                        floors_history[dungeon.level] = (dungeon, beholder)

                        # Auto-save progress
                        save_game(hero, beholder, dungeon)
                        print(f"{GREEN}Progress saved.{RESET}")

                        next_level = dungeon.level + 1

                        # Check if next level exists in history
                        if next_level in floors_history:
                            # Load existing floor
                            dungeon, beholder = floors_history[next_level]
                            hero.x, hero.y = 1, 1
                            message = f"Returned to floor {next_level}."
                        else:
                            # Generate new floor
                            dungeon = Dungeon(dungeon.size, level=next_level)
                            dungeon.create_dungeon()
                            beholder = Beholder(10, 10, level=next_level)
                            hero.x, hero.y = 1, 1
                            respawn_beholder(dungeon, beholder, hero.x, hero.y)
                            message = f"Descended to floor {next_level}."

                        # Reset floor move counter (allows 'G' only if needed immediately)
                        moves_on_floor = 0
                        continue

        else:
            message = "Unknown command."
            continue

        # Check for exhaustion (drop items if too heavy)
        if hero.stamina < hero.current_load:
            dropped_msg = []
            for item in hero.inventory[:]:
                if item.equipped:
                    item.equipped = False
                    hero.inventory.remove(item)
                    dungeon.items[(hero.x, hero.y)] = item
                    dropped_msg.append(item.name)

            if dropped_msg:
                names = ", ".join(dropped_msg)
                message += f" {RED}Collapsed from weight! Dropped: {names}!{RESET}"

        # --- ENEMY TURN ---
        if action_taken and beholder.hp > 0:
            moves_on_floor += 1  # Increment counter to disable map regen
            beholder.update(hero, dungeon.dungeon_map)

            if hero.hp <= 0:
                renderer.render(dungeon, hero, beholder, f"{RED}YOU DIED!{RESET}")
                break