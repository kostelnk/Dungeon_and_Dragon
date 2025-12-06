def game_loop(dungeon, hero, beholder, renderer):

    while True:
        renderer.render(dungeon, hero, beholder)

        cmd = input("Move (WASD), Q to quit: ").lower()

        if cmd == "q":
            print("Goodbye!")
            break

        direction = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }

        if cmd not in direction:
            continue

        dx, dy = direction[cmd]

        # Hero movement → FIXED
        hero.move(dx, dy, dungeon)

        # Beholder always gets a turn
        beholder.update(hero, dungeon.dungeon_map)

        if hero.hp <= 0:
            print("💀 You died! The Beholder devoured your soul.")
            break
