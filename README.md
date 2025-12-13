# Dungeon & Dragon

**Dungeon & Dragon** is a Python-based roguelike dungeon crawler played in the terminal. 
Explore procedurally generated maps, fight smart enemies, manage your stamina and inventory, and collect as much gold as possible on your way down.

## 🎮 Features

* **Procedural Generation:** Every floor is unique, created using random noise algorithms with connectivity checks (Flood Fill) to ensure no dead ends.
* **Smart Enemy AI:** The "Beholder" tracks you using pathfinding algorithms (BFS), navigating around walls to chase you, and keeps a safe distance when spawning.
* **RPG Mechanics:**
    * **Stamina System:** Movement and actions cost stamina. Carrying too much weight will cause you to tire faster.
    * **Inventory:** Manage weapons, shields, and potions. Drop items to reduce weight.
    * **Combat:** Turn-based combat where stats (Attack/Defense) matter.
* **Save/Load System:** Full persistence using JSON. Save your progress and resume later.
* **Cross-Platform:** Runs on Windows, Linux, and macOS (with automatic color support).

## 📋 Requirements

* Python 3.11 or higher
* No external libraries required (uses standard library only).

## 🚀 How to Run

1.  **Open your terminal/command prompt.**
2.  **Navigate to the folder** containing the `kostelnk_dungeon_game` directory.
3.  **Run the game** using the following command:

```bash
python -m kostelnk_dungeon_game.main
(Note: Thanks to the built-in path fixes, you can also run python main.py directly inside the kostelnk_dungeon_game folder).

🕹️ Controls
Key	Action
W / A / S / D	Move Up, Left, Down, Right
R	Rest (Recover Stamina)
I	Inventory (Check items, weight, and stats)
E   [item name]	Equip weapon/shield or Drink potion
X   [item name]	Drop an item to the ground
G	Regenerate Map (Only works at start pos 1,1)
Q	Quit (Prompts to save progress)
save	Manually save the game at any time


🗺️ Map Legend


@ : Hero (You)

B : Beholder (The Enemy)

▓ : Wall

. : Floor

> : Stairs (Descend to next level)

$ : Gold

/ : Weapon (Sword)

O : Shield

! : Potion

📂 Project Structure


kostelnk_dungeon_game/
│
├── main.py                # Entry point (Setup & Initialization)
├── savefile.json          # Stores your saved game data (auto-generated)
│
├── game/                  # Game Logic
│   ├── loop.py            # Main Loop (Input -> Update -> Render)
│   └── menu.py            # Main Menu UI
│
├── dungeon_core/          # Game Entities & Mechanics
│   ├── dungeon.py         # Map generation (Noise + Flood Fill)
│   ├── hero.py            # Player stats, inventory, movement
│   ├── beholder.py        # Enemy AI (BFS Pathfinding)
│   └── finds.py           # Item classes (Weapon, Potion, etc.)
│
└── game_io/               # Input/Output
    ├── renderer.py        # ASCII rendering engine
    └── save_load.py       # JSON serialization logic



🛠️ Customization
You can adjust game balance by modifying the code:

Difficulty: In dungeon_core/beholder.py, change self.attack_power or self.max_hp.

Player Stats: In dungeon_core/hero.py, adjust self.max_hp or self.max_stamina.

Map Size: In main.py, change the default map_size = (40, 15).


📝 License
Created by Kostelnk for educational purposes.
