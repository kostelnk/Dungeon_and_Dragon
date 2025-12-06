"""
Entry point for the game.
Initializes the core components and starts the game loop.
"""

import sys
import os

# Zajištění, že Python najde moduly i v podsložkách (pokud bys spouštěl script odjinud)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.dungeon import Dungeon
from core.hero import Hero
from core.beholder import Beholder
from io.renderer import Renderer
from game.loop import game_loop

def main():
    """
    Main setup and execution function.
    """
    # 1. Vytvoření Dungeonu (šířka 30, výška 15, začínáme na patře 1)
    dungeon = Dungeon((30, 15), level=1)
    dungeon.create_dungeon() #

    # 2. Vytvoření Hrdiny (startovní pozice x=2, y=2)
    # Atributy jako HP a inventář se nastaví uvnitř třídy Hero
    hero = Hero(2, 2) #

    # 3. Vytvoření Beholdera (startovní pozice x=10, y=10)
    beholder = Beholder(10, 10) #

    # 4. Inicializace Rendereru (stará se o vykreslování)
    renderer = Renderer() #

    # 5. Spuštění hlavní herní smyčky
    # Předáváme všechny instance, aby spolu mohly interagovat
    try:
        game_loop(dungeon, hero, beholder, renderer) #
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Goodbye!")
        sys.exit()

if __name__ == "__main__":
    main()
