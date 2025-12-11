import os
import sys


class MainMenu:
    """
    Handles the main menu UI and user choices.
    """

    def __init__(self):
        self.title = r"""                                              

 ████▒  █    █ ██   █  ▒███▒ ██████  ▓██▓  ██   █
 █  ▒█░ █    █ ██░  █ ░█▒ ░█ █      ▒█  █▒ ██░  █
 █   ▒█ █    █ █▒▓  █ █▒     █      █░  ░█ █▒▓  █
 █    █ █    █ █ █  █ █      █      █    █ █ █  █
 █    █ █    █ █ ▓▓ █ █   ██ ██████ █    █ █ ▓▓ █
 █    █ █    █ █  █ █ █    █ █      █    █ █  █ █
 █   ▒█ █    █ █  ▓▒█ █▒   █ █      █░  ░█ █  ▓▒█
 █  ▒█░ █▒  ▒█ █  ░██ ▒█░ ░█ █      ▒█  █▒ █  ░██
 ████▒   ████  █   ██  ▒███▒ ██████  ▓██▓  █   ██
"""

    def clear_screen(self):
        """Clears the terminal screen (Windows/Linux/Mac compatible)."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Prints the ASCII title and welcome message."""
        self.clear_screen()
        print(self.title)
        print("=" * 50)
        print("Welcome to the dungeon, hero!")
        print("=" * 50 + "\n")

    def show_mechanics(self):
        """Displays game mechanics and goals."""
        self.print_header()
        print("--- GAME MECHANICS & GOAL ---")
        print("\n[ GOAL ]")
        print("Your task is to descend deep into the dungeon.")
        print("You must find the stairs (>) to the next floor.")
        print("The legendary ARTIFACT lies on the 7th level.")
        print("Retrieve it to win the game!")

        print("\n[ ITEMS ]")
        print("⚔️  Weapons: Increase your attack. The better the sword, the faster you kill monsters.")
        print("🛡️  Shields: Increase defense. Reduce the damage you take.")
        print("🧪  Potions: Restores your health (HP) or energy.")
        print("💰  Gold:    Increases your score.")

        print("\n[ COMBAT ]")
        print("Combat happens automatically when bumping into an enemy, or turn-based.")
        print("Every step costs Stamina. If you run out, you must rest.")

        input("\n>> Press Enter to return to menu...")

    def show_controls(self):
        """Displays controls."""
        self.print_header()
        print("--- CONTROLS ---")
        print("\nMOVEMENT:")
        print("  [W] - Up")
        print("  [S] - Down")
        print("  [A] - Left")
        print("  [D] - Right")

        print("\nACTIONS:")
        print("  [R] - Restore your energy")
        print("  [I] - Inventory (see what is in your backpack)")
        print("  [E] - Equip (equip items or drink potions)")
        print("  [G] - Regenerate Map (Only works at start pos 1,1)")
        print("  [Q] - Quit game (save)")
        print("  save - to save your game write save anytime")

        print("\nMAP:")
        print("  @ = Hero (You)")
        print("  ▓ = Wall")
        print("  . = Floor")
        print("  > = Stairs down")
        print("  ? = Item / Gold")
        input("\n>> Press Enter to return to menu...")

    def run(self):
        """
        Main menu loop.
        Returns:
            str: 'new', 'load' or exits the program.
        """
        while True:
            self.print_header()
            print("1. ⚔️  NEW GAME")
            print("2. 💾  LOAD GAME")
            print("3. 📖  HOW TO PLAY (Mechanics & Goal)")
            print("4. ⌨️  CONTROLS")
            print("5. ❌  EXIT")

            print("\n" + "-" * 50)
            choice = input("Select an option (1-5): ").strip()

            if choice == '1':
                return 'new'
            elif choice == '2':
                return 'load'
            elif choice == '3':
                self.show_mechanics()
            elif choice == '4':
                self.show_controls()
            elif choice == '5':
                print("Goodbye, hero!")
                sys.exit()
            else:
                input("Invalid choice! Press Enter and try again...")