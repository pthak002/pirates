from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import math
from game.events.earthquake import Earthquake 
from game.items import TreasureChest
import game.combat as combat
import random

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'P'
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["cave"] = Cave(self)
        self.locations["waterfall"] = Waterfall(self)
        self.locations["ruins"] = Ruins(self)
        self.locations["volcano tower"] = VolcanoTower(self)

    def enter (self, ship):
        print ("Welcome! You arrived at an mysterious island. What is your command?")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach(location.SubLocation):  
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce("You arrived at the beach. You find an old, weathered map half-buried in the sand.", pause = False)
        announce("The map seems to be a rough sketch of the island, with various locations marked with symbols.", pause = False)
        announce("In the corner of the map, you notice a few lines of text:", pause = False)
        announce('"Seek the treasure that was long forgotten,', pause = False)
        announce("Solve the riddles, and your reward will be gotten.", pause = False)
        announce("Follow the path, from beach to cave,", pause = False)
        announce("Decode the message that the ancients gave.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["cave"]
        elif (verb == "east" or verb == "west"):
            announce ("You walk all the way around the island on the beach. It's not very interesting.")

class Cave(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "cave"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['solve'] = self  # Added a new verb for solving the riddle
        self.event_chance = 50
        self.events.append(Earthquake()) 

    def enter(self):
        announce("You arrive at the cave. if you type solve and enter you get something")

    def solve_riddle(self):
        announce("You see an ancient inscription on the cave wall:")
        announce("I'm light as a feather, yet the strongest man can't hold me for much more than a minute. What am I?")
        answer = input("Your answer: ").lower()
        if answer == "breath":
            announce("The cave rumbles, and a secret message is revealed, which says if you go west you will find a magical waterfall.")
            config.the_player.next_loc = self.main_location.locations["waterfall"]
        else:
            announce("The cave remains silent, your answer was incorrect.")
            config.the_player.next_loc = self  # Set next_loc to the current location (Cave)

    def process_verb(self, verb, cmd_list, nouns):
        if verb in self.verbs:
            if verb == "solve":
                self.solve_riddle()
            elif verb == "south":
                announce("You return to the beach.")
                config.the_player.next_loc = self.main_location.locations["beach"]
            elif verb == "west":
                config.the_player.next_loc = self.main_location.locations["waterfall"]
            elif verb == "north" or verb == "west":
                announce("You walk all the way around the cave on the beach. It's not very interesting.")
        else:
            announce("You can't do that here.")


class Waterfall(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "waterfall"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['heal'] = self
        self.event_chance = 50

    def enter(self):
        announce("Arrived at the waterfall. You find a flower that will heal wounds.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You go to the ruins.")
            config.the_player.next_loc = self.main_location.locations["ruins"]
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["cave"]
        elif verb == "north" or verb == "west":
            announce("You walk all the way around the waterfall on the beach. It's not very interesting.")
        elif verb == "heal":
            for i in config.the_player.get_pirates():
                i.health = 100
                i.print()
            print("Your wounds are healed.")        


class Ruins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        announce("You arrived at the ruins'")
        monsters = []
        monsters.append(RuinsMonster("Ruins Monster 1"))
        monsters.append(RuinsMonster("Ruins Monster 2"))
        announce ("You are attacked by monsters")
        combat.Combat(monsters).combat()
        self.handle_monster_loot()

    def handle_monster_loot(self):
        for pirate in config.the_player.get_pirates():
            powerful_firearm = items.AncientBlunderbuss()
            pirate.items.append(powerful_firearm)
            announce(f"{pirate.name} obtained a {powerful_firearm.name}!")
    

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You go to the volcano tower.")
            config.the_player.next_loc = self.main_location.locations["volcano tower"]
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["waterfall"]
        elif verb == "east" or verb == "west":
            announce("You walk all the way around the ruins. It's not very interesting.")


class VolcanoTower (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "volcano tower"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['solve'] = self

    def enter (self):
        announce("You arrived at the volcano tower. You see a stone with an inscription:")
        announce("To proceed, you must decipher the code. It consists of two digits. ")
        announce("The first digit is a number between 1 and 4. ")
        announce("the second digit is the factorial of the first digit. What is the code?'")
        announce("type solve to enter the code")

    def treasure_chest(self):
        for pirate in config.the_player.get_pirates():
            treasure_chest = items.TreasureChest()
            pirate.items.append(treasure_chest)
            announce(f"{pirate.name} obtained a {treasure_chest.name}!")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["ruins"]
        elif (verb == "south" or verb == "west"):
            announce ("You walk all the way around the cave on the beach. It's not very interesting.")
        elif verb == "solve":
            answer = input("Enter the code (two digits): ")
            if len(answer) == 2 and answer.isdigit():
                first_digit = int(answer[0])
                second_digit = int(answer[1])
                if first_digit in range(1, 5) and second_digit == math.factorial(first_digit):
                    announce("The stone rumbles, gives you the treasure")
                    self.treasure_chest()
                else:
                    announce("Nothing happens. The code seems incorrect.")
            else:
                announce("Invalid input. Please enter a two-digit number.")
#whatever

class RuinsMonster(combat.Monster):
    def __init__(self,name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        attacks["spike with claws"] = ["spike with claws",random.randrange(35,51), (1,10)]
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
       