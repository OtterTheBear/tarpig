#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import sys

#class Game:
#    def __init__(self, loc, move, file)



class Loc:
    def __init__(self, cord, name):
        self.cord = cord
        self.name = name


class Player:
    def __init__(self, name, hp, mhp, living, inv, loc):
        self.name = name
        self.hp = hp
        self.mhp = mhp
        self.living = living
        self.inv = inv
        if len(self.inv) > 1:
            self.holding = inv[0]
            self.wearing = inv[1]
        self.loc = loc

    def health(self):
        output = "["
        for x in range(1, self.mhp+1):
            if x <= self.hp:
                output += "\u2588"
            else:
                output += "\u2591"
        output += "]"
        print(f"@{self.name}: HP:", output, str(self.hp)+"/"+str(self.mhp))

    def setHP(self, newHP):
        self.hp = newHP
        if self.hp > self.mhp:
            self.hp = self.mhp
        if self.hp <= 0:
            self.living = False
            self.hp = 0

    def getLoc(self):
        print(f"@{self.name}: Location: {self.loc.name}.")

    def heal(self, heal):
        if isinstance(heal, Heal):
            if heal in self.inv:
                self.setHP(self.hp + heal.amount)
                print(f"@{self.name}: Healed. ", end="")
                self.health()
            else:
                print(f"@{self.name}: {heal.name} is not in your inventory.")
        else:
            print(f"@{self.name}: {heal.name} is not a heal.")
    
    def attack(self, target):
        if isinstance(target, Player):
            if isinstance(self.holding, Weapon):
                target.setHP(target.hp-self.holding.dmg)
                print(f"@{self.name}: {target.name} took {self.holding.dmg} damage. ({str(target.hp)}/{str(target.mhp)})")
            else:
                print(f"@{self.name}: {self.holding.name} is not a weapon.")
        else:
            print(f"@{self.name}: {target.name} is not a person/animal")

    def getinv(self):
        for x in self.inv:
            print(x.name)

    def addinv(self, item):
        self.inv.append(item)


class Item:
    def __init__(self, name, desc, owner):
        self.name = name
        self.desc = desc
        self.owner = owner
        self.owner.inv.append(self)


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
emptyplayer = Player("emptyplayer", 3000, 3000, True, [], "")
emptyobj0 = Item("empty0", "", emptyplayer)


castle = Loc(5, "castle")
# hmm = Player("hmm", 5, 10, True, [], poop, "apple", castle)
# smh = Player("smh", 5, 10, True, [], poop, "apple", castle)

# hmm.health()
# smh.attack(hmm)
# hmm.getLoc()
emptyplayer.getinv()
# print("Is hmm living?", hmm.living)
print("You are standing in a field")
input("hmm")
