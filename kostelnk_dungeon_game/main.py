"""
Main entry point for the Dungeon game.
"""
import sys
import os
import random

# Adjust imports to match your folder structure
from kostelnk_dungeon_game.game.menu import MainMenu
from kostelnk_dungeon_game.dungeon_core.dungeon import Dungeon
from kostelnk_dungeon_game.dungeon_core.hero import Hero
from kostelnk_dungeon_game.dungeon_core.beholder import Beholder
from kostelnk_dungeon_game.game.loop import game_loop
from kostelnk_dungeon_game.game_io.renderer import Renderer
from kostelnk_dungeon_game.game_io.save_load import load_game

# Colors for the logo
RED = "\033[91m"
RESET = "\033[0m"

def print_logo():
    """Prints the ASCII game logo."""
    logo = r"""
 ____  _   _ _   _  ____  ____  ____  _   _ 
|  _ \| | | | \ | |/ ___|/ __||/ ___|| \ | |
| | | | | | |  \| | |  _| |_ _ \___ \|  \| |
| |_| | |_| | |\  | |_| | |___  ___) | |\  |
|____/ \___/|_| \_|\____|\____||____/|_| \_|
    """
    print(f"{RED}{logo}{RESET}")
    print("       (Created in Python)\n")

def main():
    # 0. Show Logo
    print_logo()

    # 1. Show Menu
    menu = MainMenu()
    action = menu.run()

    # 2. Initialize Game Objects
    hero = None
    dungeon = None
    beholder = None
    renderer = Renderer()

    # Default settings
    map_size = (40, 15)
    current_level = 1

    if action == 'new':
        print("\nGenerating new dungeon...")

        # Create Dungeon
        dungeon = Dungeon(size=map_size, level=current_level)
        dungeon.create_dungeon()

        # Create Hero (Safe start at 1,1 or center of first room)
        start_x, start_y = dungeon.get_valid_start_position()
        hero = Hero(x=start_x, y=start_y)

        # --- Spawn Beholder (Far away from Hero) ---
        possible_targets = []

        # Find tiles that are at least 5 steps away
        for (tx, ty) in dungeon.floor_tiles:
            dist_x = abs(tx - start_x)
            dist_y = abs(ty - start_y)
            if dist_x >= 5 or dist_y >= 5:
                possible_targets.append((tx, ty))

        # Select spawn position
        if possible_targets:
            bx, by = random.choice(possible_targets)
        elif dungeon.floor_tiles:
            # Fallback for small maps
            bx, by = random.choice(dungeon.floor_tiles)
        else:
            # Emergency fallback
            bx, by = start_x, start_y

        # Create Beholder
        beholder = Beholder(x=bx, y=by, level=current_level)

        print("Game ready! Entering the darkness...")
        input("Press Enter to start...")

    elif action == 'load':
        print("\nLoading saved game...")
        if os.path.exists("savefile.json"):
            # Init empty objects
            dungeon = Dungeon(size=map_size, level=1)
            hero = Hero(0, 0)
            beholder = Beholder(0, 0)

            try:
                load_game(hero, beholder, dungeon, path="savefile.json")
                print("Game loaded successfully!")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"Error loading save file: {e}")
                input("Press Enter to start a NEW GAME instead...")
                # Recursively restart main to try again or pick New Game
                return main()
        else:
            print("No save file found! Starting new game.")
            input("Press Enter...")

            # Fallback to New Game logic
            dungeon = Dungeon(size=map_size, level=current_level)
            dungeon.create_dungeon()
            start_x, start_y = dungeon.get_valid_start_position()
            hero = Hero(x=start_x, y=start_y)

            # Simple fallback spawn
            if dungeon.floor_tiles:
                bx, by = random.choice(dungeon.floor_tiles)
            else:
                bx, by = 1, 1
            beholder = Beholder(bx, by, level=current_level)

    # 3. Start Game Loop
    if hero and dungeon and beholder:
        game_loop(dungeon, hero, beholder, renderer)
    else:
        print("Error: Could not initialize game state.")


if __name__ == "__main__":
    main()