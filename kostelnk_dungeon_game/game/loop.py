import sys
from io.save_load import save_game, load_game
from core.dungeon import Dungeon
from core.beholder import Beholder


def game_loop(dungeon, hero, beholder, renderer):
    """
    Main game loop handling input and updates.
    """
    message = "Welcome to the Dungeon! Press WASD to move."

    # Store visited floors to return to them later
    floors_history = {}  # {level_int: (dungeon_obj, beholder_obj)}

    while True:
        # 1. Render
        renderer.render(dungeon, hero, beholder, message)
        message = ""  # Clear message after print

        # 2. Input
        cmd_raw = input("Action (WASD, I=Inv, E=Equip, Save/Load, Q=Quit): ").lower().split()
        if not cmd_raw: continue
        cmd = cmd_raw[0]

        # --- Movement ---
        dx, dy = 0, 0
        if cmd == 'w':
            dy = -1
        elif cmd == 's':
            dy = 1
        elif cmd == 'a':
            dx = -1
        elif cmd == 'd':
            dx = 1

        # --- Meta Commands ---
        elif cmd == 'q':
            print("Goodbye!")
            sys.exit()

        elif cmd == 'save':
            save_game(hero, beholder, dungeon)
            message = "Game saved."
            continue

        elif cmd == 'load':
            # Note: Ideally load_game should return new objects
            load_game(hero, beholder, dungeon)
            message = "Game loaded."
            continue

        elif cmd == 'i':
            print("\n=== INVENTORY ===")
            for item in hero.inventory:
                status = "[E]" if item.equipped else "   "
                print(f"{status} {item.name} ({item.type})")
            input("Press Enter to continue...")
            continue

        elif cmd == 'e':
            # Simplified equip by name match
            if len(cmd_raw) < 2:
                message = "Usage: e <item_name>"
            else:
                target_name = " ".join(cmd_raw[1:])
                # Toggle equip logic could go here
                hero.equip_item(target_name)
                message = f"Tried to equip {target_name}"
            continue

        else:
            message = "Unknown command."
            continue

        # 3. Process Movement
        if dx != 0 or dy != 0:
            moved = hero.move(dx, dy, dungeon)
            if moved:
                # Decrease Stamina (optional as per assignment)
                if not hasattr(hero, 'stamina'): hero.stamina = 50
                hero.stamina -= 1

                # Check for Item Pickup
                item = dungeon.get_item_at(hero.x, hero.y)
                if item:
                    hero.add_item(item)
                    message = f"You picked up {item.name}!"

                # Check for Stairs
                if dungeon.dungeon_map[hero.y][hero.x] == ">":
                    # Save current state
                    floors_history[dungeon.level] = (dungeon, beholder)

                    next_level = dungeon.level + 1

                    # Check if we visited next floor before (simple persistence)
                    if next_level in floors_history:
                        dungeon, beholder = floors_history[next_level]
                        # Reset hero position near entrance (simplified)
                        hero.x, hero.y = 1, 1
                        message = f"You returned to floor {next_level}."
                    else:
                        # Generate new floor
                        dungeon = Dungeon(dungeon.size, level=next_level)
                        dungeon.create_dungeon()
                        # Spawn new Beholder for deep floor
                        beholder = Beholder(10, 10)
                        hero.x, hero.y = 1, 1
                        message = f"You descended to floor {next_level}."

            # 4. Enemy Turn
            if beholder.hp > 0:
                beholder.update(hero, dungeon.dungeon_map)
                if hero.hp <= 0:
                    renderer.render(dungeon, hero, beholder, "YOU DIED!")
                    break
