## Import Classes and Libraries

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import item
import random

## Creating spells & items
# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 35, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create some Items
potion = item("Potion", "potion", "Heals 100 HP", 100)
hipotion = item("Hi-Potion", "potion", "Heals 200 HP", 200)
superpotion = item("Super Potion", "potion", "Heals 1500 HP", 1500)
elixer = item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = item("Grenade", "attack", "Deals 1000 damage", 1000)

# Sub Magic
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, meteor, cure]
enemy_spells_boss = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# Instantiate People

player1 = Person("Valos:", 3260, 300, 310, 34, player_spells, player_items)
player2 = Person("Remos:", 4160, 440, 325, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 300, 288, 34, player_spells, player_items)
enemy1 = Person("Impis", 1250, 130, 200, 325, enemy_spells, [])
enemy2 = Person("Magus", 13000, 700, 525, 25, enemy_spells_boss, [])
enemy3 = Person("Impus", 1250, 130, 200, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "ENEMIES ATTACK!" + bcolors.ENDC)
defeated_enemies = 0
defeated_players = 0
while running:
    print("=====================")

    print("\n")
    print(bcolors.BOLD + "NAME                    HP                                       MP" + bcolors.ENDC)
    for player in players:
        player.get_stats()
    print("\n")

    print(bcolors.BOLD + "NAME                     Enemy HP                                                          " +
          "Enemy MP" + bcolors.ENDC)
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            if enemies[enemy].get_hp() > 0:
                enemies[enemy].take_damage(dmg)
                print(bcolors.BOLD + player.name[0:5] + " attacks " + enemies[enemy].name[0:5] + " for", dmg,
                      "points of damage." + bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemy].name + " has died." + bcolors.ENDC)
                del enemies[enemy]
                defeated_enemies += 1
                if defeated_enemies == 3:
                    print("\n" + bcolors.OKGREEN + "Congratulations, you've defeated the enemy!" + bcolors.BOLD +
                          " You win!" + bcolors.ENDC)
                    running = False

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if magic_choice == -1:
                continue

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP left\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " +
                      enemies[enemy].name[0:5] + "." + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemy].name + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1
                    if defeated_enemies == 3:
                        print("\n" + bcolors.OKGREEN + "Congratulations, you've defeated the enemy!" + bcolors.BOLD +
                              " You win!" + bcolors.ENDC)
                        running = False


        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left in your inventory..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " points." + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores all HP/MP." + bcolors.ENDC)
                if item.name == "Elixer":
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage to " +
                      enemies[enemy].name[0:5] + "." + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("\n" + bcolors.FAIL + bcolors.BOLD + enemies[enemy].name + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1
                    if defeated_enemies == 3:
                        print("\n" + bcolors.OKGREEN + "Congratulations, you've defeated the enemy!" + bcolors.BOLD +
                              " You win!" + bcolors.ENDC)
                        running = False

    print("\n" + "=====================")

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy.get_hp() > 0:
            if enemy_choice == 0 and enemy.get_hp() > 0.1*enemy.get_max_hp():
                notattacked = True
                while notattacked:
                    # target = random.randrange(0, len(players))
                    target = 0
                    enemy_dmg = enemy.generate_damage()
                    if players[target].get_hp() > 0:
                        players[target].take_damage(enemy_dmg)
                        print(str(enemy.name) + " attacks " + players[target].name[0:5] +
                              " for", enemy_dmg, "points of damage." + bcolors.ENDC)
                        notattacked = False
                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(":", "") + " has died." +
                          bcolors.ENDC + "\n")
                    del players[target]
                    defeated_players += 1
                    if defeated_players == 3:
                        print("Oh dear, looks like everyone has been defeated." + bcolors.FAIL + bcolors.BOLD + " You lose."
                              + bcolors.ENDC)
                        running = False

            if enemy_choice == 1 or enemy.get_hp() < 0.20*enemy.get_max_hp():
                spell, magic_dmg = enemy.choose_enemy_spell()
                current_enemy_mp = enemy.get_mp()
                enemy.reduce_mp(spell.cost)

                if spell.type == "white":
                    enemy.heal(magic_dmg)
                    print(bcolors.FAIL + enemy.name + " heals self with " + spell.name + " for " + str(magic_dmg) +
                          " HP." + bcolors.ENDC)
                elif spell.type == "black":
                    notattacked = True
                    while notattacked:
                        # target = random.randrange(0, len(players))
                        target = 0
                        if players[target].get_hp() > 0:
                            players[target].take_damage(magic_dmg)
                            print(bcolors.OKBLUE + enemy.name + " casts " + spell.name + " with " + str(magic_dmg),
                                  "points of damage to " + players[target].name[0:5] + "." + bcolors.ENDC)
                            notattacked = False
                            if players[target].get_hp() == 0:
                                print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(":", "") + " has died." +
                                      bcolors.ENDC + "\n")
                                del players[target]
                                defeated_players += 1
                                if defeated_players == 3:
                                    print(
                                        "Oh dear, looks like everyone has been defeated." + bcolors.FAIL + bcolors.BOLD +
                                        " You lose." + bcolors.ENDC)
                                    running = False


    # for enemy in enemies:
    #     if enemy.get_hp() == 0:
    #         defeated_enemies += 1
    # if defeated_enemies == 3:
    #     print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
    #     running = False
    #
    # defeated_players = 0
    # for player in players:
    #     if player.get_hp() == 0:
    #         defeated_players += 1
    # if defeated_players == 3:
    #     print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
    #     running = False