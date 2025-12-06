"""
Entry point for the game.
"""

from kostelnk_dungeon_game.core.dungeon import Dungeon
from kostelnk_dungeon_game.core.hero import Hero
from kostelnk_dungeon_game.core.beholder import Beholder
from kostelnk_dungeon_game.io.renderer import Renderer
from kostelnk_dungeon_game.game.loop import game_loop


def main():
    dungeon = Dungeon((30, 15))
    dungeon.create_dungeon()

    hero = Hero(2, 2)
    beholder = Beholder(10, 10)

    renderer = Renderer()

    game_loop(dungeon, hero, beholder, renderer)


if __name__ == "__main__":
    main()
