# 🛡️ Turn-Based Combat System (Python)

A simple turn-based combat system implemented in Python. This project simulates a battle between a player and a group of enemies, using basic RPG-like mechanics such as attack, defense, speed, status effects (like poison), and a combat turn queue.

---

## 📖 Project Description

This project includes:

- A `Character` class that represents both the player and enemies with attributes like health, attack, defense, speed, and status effects.
- A `Combat` class that handles the turn-based logic, including:
  - Speed-based turn ordering
  - Damage calculation with critical hit chance
  - Status effects like poison
  - Enemy AI that attacks the player
  - Combat log output

The system is entirely text-based and designed to run in the terminal.

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.x installed on your system

> No external libraries are required — only Python's built-in `random` module is used.

---

## 🚀 How to Run the Code

1. **Clone or download** the project files.
```bash
   git clone https://github.com/ajayy-m/RPG-Combat-Sim.git cd RPG-Combat-Sim
```
2. Open a terminal or command prompt.

3. Navigate to the project directory where the `.py` file is located.

4. Run the script using:

```bash
   python combat_system.py
```

---

## 🕹️ How It Works

* The game starts with one player and two enemies (Goblin and Orc).
* Each character takes turns based on their speed.
* On the player’s turn, you’ll be prompted to select an enemy to attack.
* On enemy turns, each living enemy attacks the player.
* Poison may be applied randomly and deals damage over time.
* The combat loop continues until either:

  * All enemies are defeated (Victory!), or
  * The player is defeated (Defeat).

---

## 📝 Additional Notes and Assumptions

* Critical hits have a **10% chance** to deal **1.5× damage**.
* Poison has a **20% chance** to be inflicted on an enemy after a player attack.
* Poison deals **5 damage per turn** for **3 turns**.
* The combat log is printed after each round for clarity.
* Input validation is included for target selection.

---

## 📄 License

This project is licensed on Apache 2.0
