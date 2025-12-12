"""
Main entry point for the Dungeon game.
"""
import sys
import os

# --- Module Search Path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# --- Windows Colors ---
if os.name == 'nt':
    os.system('color')


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


def initialize_new_game(map_size, level):
    """
    Helper function to generate a fresh Dungeon, Hero, and Beholder.
    """
    # 1. Create Dungeon
    dungeon = Dungeon(size=map_size, level=level)
    dungeon.create_dungeon()

    # 2. Create Hero (Safe start at 1,1)
    start_x, start_y = dungeon.get_valid_start_position()
    hero = Hero(x=start_x, y=start_y)

    # 3. Create Beholder
    # FIX: Instantiate Beholder FIRST, then move it
    beholder = Beholder(x=0, y=0, level=level)
    beholder.spawn_at_safe_location(dungeon.floor_tiles, hero.x, hero.y)

    return dungeon, hero, beholder


def main():
    """
    Main execution function. Initializes the game and starts the loop.
    """
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
        dungeon, hero, beholder = initialize_new_game(map_size, current_level)

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
                return main()
        else:
            print("No save file found! Starting new game.")
            input("Press Enter...")

            dungeon, hero, beholder = initialize_new_game(map_size, current_level)

    # 3. Start Game Loop
    if hero and dungeon and beholder:
        game_loop(dungeon, hero, beholder, renderer)
        return None

    print("Error: Could not initialize game state.")
    return None


if __name__ == "__main__":
    main()
