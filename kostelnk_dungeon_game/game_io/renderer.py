"""
ASCII renderer for dungeon maps and HUD.
"""

import os

class Renderer:
    """
    Handles drawing the game state to the console.
    """

    def render(self, dungeon, hero, beholder=None, message=""):
        """
        Clears screen and prints map + status.
        """
        # Clear console (cross-platform)
        os.system('cls' if os.name == 'nt' else 'clear')

        w, h = dungeon.size

        # Create display buffer
        display = [row[:] for row in dungeon.dungeon_map]

        # Draw Items & Gold
        for (ix, iy), item in dungeon.items.items():
            symbol = "?"
            color = "\033[96m"  # CYAN (basic items)

            if item.type == "gold":
                symbol = "$"
                color = "\033[93m"  # YELLOW (just gold)
            elif item.type == "weapon":
                symbol = "/"
            elif item.type == "shield":
                symbol = "O"
            elif item.type == "potion":
                symbol = "!"

            # Vykreslení se správnou barvou
            display[iy][ix] = f"{color}{symbol}\033[0m"
        # Draw Hero
        display[hero.y][hero.x] = f"\033[92m@\033[0m" # Green

        # Draw Beholder
        if beholder and beholder.hp > 0:
            display[beholder.y][beholder.x] = beholder.symbol

        # Print Map
        print(f" --- FLOOR {dungeon.level} ---")
        for row in display:
            print("".join(row))

        # HUD
        print("-" * 50)
        print(f"HP: {hero.hp} | Stm: {getattr(hero, 'stamina', 50)} | Gold: {hero.gold}")
        print(f"Stats: ATK {hero.attack} | DEF {hero.defense}")
        print(f"Leave game press: Q")
        print("-" * 50)

        # Message Log
        if message:
            print(f"> {message}")