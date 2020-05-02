#! /usr/bin/python3
# This is just a bunch of class definitions
import sys
"""
class Game:
    def __init__(self, loc, move, file)
"""


class Loc:
    def __init__(self, cord, name, objs):
        self.cord = cord
        self.name = name
        self.objs = [] ###################################################


class Player:
    def __init__(self, hp, mhp, inv):
        self.hp = hp
        self.mhp = mhp
        self.inv = inv

    def health(self):
        output = "["
        for x in range(1, self.mhp+1):
            if x <= self.hp:
                output += "\u2588" # The native python IDE literally doesn't support a feature of python. Not "\UXXXXXXXX" only "\uXXXX"
            else:
                output += "\u2591"
        output += "]"
        print("Your HP is ", output, str(self.hp)+"/"+str(self.mhp))

    def setHP(self, newHP):
        self.hp = newHP
        if self.hp > self.mhp:
            self.hp = self.mhp

    def heal(self, heal):
        if isinstance(heal, Heal):
            self.setHP(self.hp + heal.amount)
            print("Healed. ", end="")
            self.health()
        else:
            print(f"{heal} is not a heal.")
    
    def getinv(self):
        for x in self.inv:
            print(x)

    def addinv(self, item):
        inv.append(item)


class Item:
    def __init__(self, name, desc, owner):
        self.name = name
        self.desc = desc


class Heal(Item):
    def __init__(self, name, desc, owner, amount):
        Item.__init__(self, name, desc, owner)
        self.amount = amount


sys.stdout.write("\033[2J\033[H")
print("TaRPiG - Text Roleplaying game")

hmm = Player(5, 10, ["car", "apple", "banana"])
print("You are in a field")
awesom = Heal("poop", "some poop", "some guy", 5)
hmm.health()
hmm.heal(awesom)
print(isinstance(awesom, Item))
a = input("hmm")
