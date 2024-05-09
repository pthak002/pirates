import random
import game.event as event
from game.display import announce
from game.player import Player
from game.context import Context
import game.config as config

class Earthquake(Context, event.Event):
    def __init__(self):
        super().__init__()
        self.name = "Earthquake"
        self.verbs = {
            'help': self,
            'search': self,
            'flee': self
        }
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "help":
            print("After an earthquake, you can search for survivors or flee the area.")
            self.go = False
        elif verb == "search":
            r = random.randint(1, 10)
            if r < 5:
                self.result["message"] = "You found a few survivors and helped them escape."
            else:
                self.result["message"] = "Unfortunately, you didn't find any survivors."
            self.go = True
        elif verb == "flee":
            self.result["message"] = "You quickly fled the area to safety."
            self.go = True
        else:
            print("Invalid action. Please try again.")
            self.go = False

    def process(self, world):
        announce("The ground starts to shake violently!")
        announce("An earthquake is happening on the island!")
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "An earthquake has occurred! What do you want to do?"
        while not self.go:
            Player.get_interaction([self])
        return self.result
    