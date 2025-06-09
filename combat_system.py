import random

class Character:
    """
    Represents a character in the combat system (player or enemy).
    Each character has attributes like health, attack, defense, speed, and status effects.
    """
    def __init__(self, name, health, max_health, attack, defense, speed):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.status_effects = {}

    def is_alive(self):
        """
        Check if the character is still alive.
        """
        return self.health > 0

    def apply_status_effects(self):
        """
        Apply ongoing effects like Poison. Each effect affects health or other stats.
        """
        log = []
        if "Poison" in self.status_effects:
            damage = 5
            self.health -= damage
            self.status_effects["Poison"] -= 1
            log.append(f"{self.name} takes {damage} poison damage!")
            if self.status_effects["Poison"] <= 0:
                del self.status_effects["Poison"]
                log.append(f"{self.name} is no longer poisoned.")
        return log

    def take_damage(self, damage):
        """
        Reduce the character's health by the specified damage amount.
        """
        self.health = max(0, self.health - damage)

    def apply_poison(self, turns=3):
        """
        Apply poison effect for a specified number of turns.
        """
        self.status_effects["Poison"] = turns


class Combat:
    """
    Manages the turn-based combat between a player and a list of enemy characters.
    Handles turns, damage calculations, combat log, and status effects.
    """
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.turn_queue = sorted([player] + enemies, key=lambda c: -c.speed)  # Higher speed acts first
        self.combat_log = []

    def is_combat_over(self):
        """
        Check if the combat is over (player dead or all enemies dead).
        """
        return not self.player.is_alive() or all(not enemy.is_alive() for enemy in self.enemies)

    def is_player_turn(self):
        """
        Check if it is currently the player's turn.
        """
        return self.turn_queue[0] == self.player

    def next_turn(self):
        """
        Move the current character to the end of the turn queue if still alive.
        """
        current = self.turn_queue.pop(0)
        if current.is_alive():
            self.turn_queue.append(current)

    def damage_formula(self, attacker, defender):
        """
        Calculate the damage dealt by attacker to defender using:
        damage = max(1, attacker.attack - defender.defense // 2)
        Also handles critical hits (10% chance to deal 1.5x damage).
        """
        base_damage = max(1, attacker.attack - (defender.defense // 2))
        if random.random() < 0.10:
            base_damage = int(base_damage * 1.5)
            self.combat_log.append("Critical hit!")
        return base_damage

    def player_turn(self, target_index):
        """
        Executes the player's turn, targeting an enemy by index.
        Applies damage and may poison the enemy (20% chance).
        """
        if target_index < 0 or target_index >= len(self.enemies):
            self.combat_log.append("Invalid target.")
            return
        target = self.enemies[target_index]
        if not target.is_alive():
            self.combat_log.append(f"{target.name} is already defeated.")
            return

        damage = self.damage_formula(self.player, target)
        target.take_damage(damage)
        self.combat_log.append(f"You attacked {target.name} for {damage} damage.")

        # 20% chance to apply poison
        if random.random() < 0.2:
            target.apply_poison()
            self.combat_log.append(f"{target.name} is poisoned!")

        self.next_turn()

    def process_enemy_turns(self):
        """
        Processes enemy turns automatically.
        Each enemy attacks the player and applies any status effects.
        """
        while not self.is_player_turn() and not self.is_combat_over():
            enemy = self.turn_queue[0]
            if enemy.is_alive():
                self.combat_log.append(f"\nEnemy Turn: {enemy.name}")

                # Apply status effects like poison
                status_log = enemy.apply_status_effects()
                self.combat_log.extend(status_log)

                if enemy.is_alive():
                    damage = self.damage_formula(enemy, self.player)
                    self.player.take_damage(damage)
                    self.combat_log.append(f"{enemy.name} attacks you for {damage} damage.")
            self.next_turn()

    def print_combat_log(self):
        """
        Display the most recent combat actions and then clear the log.
        """
        for line in self.combat_log:
            print(line)
        self.combat_log.clear()


# === Game Runner ===
if __name__ == "__main__":
    # Create player and enemy characters
    player = Character("Hero", 50, 100, 15, 10, 12)
    enemy1 = Character("Goblin", 30, 30, 8, 5, 10)
    enemy2 = Character("Orc", 50, 50, 12, 8, 8)

    # Start the combat
    combat = Combat(player, [enemy1, enemy2])

    # Main combat loop
    while not combat.is_combat_over():
        print(f"\n--- Current Status ---")
        print(f"Player HP: {player.health}/{player.max_health}")
        for i, enemy in enumerate(combat.enemies, 1):
            status = "DEAD" if not enemy.is_alive() else f"{enemy.health}/{enemy.max_health}"
            print(f"Enemy {i} ({enemy.name}) HP: {status}")
        
        # Player's turn
        if combat.is_player_turn():
            print("\nYour Turn!")
            print("Choose your target:")
            for i, enemy in enumerate(combat.enemies, 1):
                if enemy.is_alive():
                    print(f"{i}. {enemy.name} (HP: {enemy.health}/{enemy.max_health})")
            try:
                target_idx = int(input("Select target number: ")) - 1
                combat.player_turn(target_idx)
            except ValueError:
                print("Invalid input. Skipping turn.")
                combat.next_turn()
        else:
            # Enemies act
            combat.process_enemy_turns()

        # Show what happened in this round
        combat.print_combat_log()

    # Final result
    if player.health > 0:
        print("\n🏆 Victory! All enemies defeated!")
    else:
        print("\n💀 Defeat! You were defeated in combat.")
