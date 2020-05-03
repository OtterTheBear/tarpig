#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import sys

#class Game:
#    def __init__(self, loc, move, file)



class Loc:
    def __init__(self, cord, name, objs):
        self.cord = cord
        self.name = name
        self.objs = objs


class Player:
    def __init__(self, hp, mhp, inv, living, holding, wearing):
        self.hp = hp
        self.mhp = mhp
        self.inv = inv
        self.living = living
        self.holding = holding
        self.wearing = wearing

    def health(self):
        output = "["
        for x in range(1, self.mhp+1):
            if x <= self.hp:
                output += "\u2588"
            else:
                output += "\u2591"
        output += "]"
        print("HP: ", output, str(self.hp)+"/"+str(self.mhp))

    def setHP(self, newHP):
        self.hp = newHP
        if self.hp > self.mhp:
            self.hp = self.mhp
        if self.hp <= 0:
            self.living = False
            self.hp = 0

    def heal(self, heal):
        if isinstance(heal, Heal):
            if heal in self.inv:
                self.setHP(self.hp + heal.amount)
                print("Healed. ", end="")
                self.health()
            else:
                print(f"{heal.name} is not in your inventory.")
        else:
            print(f"{heal.name} is not a heal.")
    
    def attack(self, target):
        target.setHP(target.hp-self.holding.dmg)

    def getinv(self):
        for x in self.inv:
            print(x)

    def addinv(self, item):
        self.inv.append(item)


class Item:
    def __init__(self, name, desc, owner):
        self.name = name
        self.desc = desc
        self.owner = owner


class Heal(Item):
    def __init__(self, name, desc, owner, amount):
        Item.__init__(self, name, desc, owner)
        self.amount = amount

class Weapon(Item):
    def __init__(self, name, desc, owner, dmg):
        Item.__init__(self, name, desc, owner)
        self.dmg = dmg


sys.stdout.write("\033[2J\033[H")
print("TaRPiG - Text Roleplaying game")
ayy = Weapon("ayy", "", "h", 5)
hmm = Player(5, 10, [ayy, "apple", "banana"], True, ayy, "apple")
smh = Player(5, 10, [ayy, "apple", "banana"], True, ayy, "apple")
awesom = Heal("poop", "some poop", "some guy", 5)

hmm.health()
smh.attack(hmm)
hmm.health()
print("Is hmm living?", hmm.living)
print("You are standing in a field")
input("hmm")
