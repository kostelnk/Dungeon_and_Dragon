"""
ASCII renderer for dungeon maps.
"""

class Renderer:
    """
    Renders the dungeon map along with hero and enemy positions.
    """

    def render(self, dungeon, hero, beholder=None):
        """
        Print dungeon map with entities drawn on top.
        """
        w, h = dungeon.size

        # Create a copy of the map to draw into
        display = [row[:] for row in dungeon.dungeon_map]

        # Draw hero
        display[hero.y][hero.x] = "@"

        # Draw Beholder if present
        if beholder:
            display[beholder.y][beholder.x] = "B"

        # Print the map
        for row in display:
            print("".join(row))

        # Print HUD
        print(f"\nHP: {hero.hp}   Gold: {hero.gold}")
