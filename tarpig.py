#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import sys

red = "\x1b[1;31m"
green = "\x1b[1;92m"
reset = "\x1b[1;0m"

#class Game:
#    def __init__(self, loc, move, file)



class Loc:
    def __init__(self, cord, name):
        self.cord = cord
        self.name = name


class Player:
    def __init__(self, name, hp, mhp, inv, loc):
        self.name = name
        self.hp = hp
        self.mhp = mhp
        self.living = (self.hp > 0)
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
        print(f"@{self.name}: HP: {output} {self.hp}/{self.mhp}")

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
                print(red + f"ERROR: @{self.name}: {heal.name} is not in your inventory." + reset)
        else:
            print(red + f"ERROR: @{self.name}: {heal.name} is not a heal." + reset)

    def getinv(self):
        output = f"@{self.name}: Inventory:\n"
        for x in self.inv:
            if x == self.inv[0]:
                output += " *"+ x.name + "\n"
            elif x == self.inv[1]:
                output += "**" + x.name + "\n"
            else:
                output += "  " + x.name + "\n"
        output += "\b\b\b\b"
        print(output)

    def addinv(self, item):
        self.inv.append(item)

    
    def attack(self, target):
        if isinstance(target, Player):
            if isinstance(self.holding, Weapon):
                target.setHP(target.hp-self.holding.dmg)
                print(f"@{self.name}: {target.name} took {self.holding.dmg} damage. ({str(target.hp)}/{str(target.mhp)})")
            else:
                print(red + f"ERROR: @{self.name}: {self.holding.name} is not a weapon." + reset)
        else:
            print(red + f"ERROR: @{self.name}: {target.name} is not a person/animal" + reset)


class Item:
    def __init__(self, name, desc, owner):
        self.name = name
        self.desc = desc
        self.owner = owner
        self.owner.inv.append(self)
        owner.__init__(owner.name, owner.hp, owner.mhp, owner.inv, owner.loc)


class Heal(Item):
    def __init__(self, name, desc, owner, amount):
        Item.__init__(self, name, desc, owner)
        self.amount = amount

class Weapon(Item):
    def __init__(self, name, desc, owner, dmg):
        Item.__init__(self, name, desc, owner)
        self.dmg = dmg


class Cmd:
    def __init__(self, name, func, *args):
        self.name = name
        self.func = func
        self.args = args

print("\x1b[2J\x1b[H")
print("TaRPiG - Text Roleplaying game")
emptyplayer = Player("emptyplayer", 3000, 3000, [], "")
emptyobj0 = Item("empty0", "", emptyplayer)
emptyobj1 = Item("empty1", "", emptyplayer)
emptyobj2 = Item("empty2", "", emptyplayer)
emptyobj3 = Item("empty3", "", emptyplayer)

emptyweapon0 = Weapon("emptyweapon0", "", emptyplayer, 28)

testplayer = Player("testplayer", 29, 30, [emptyobj0, emptyobj1, emptyobj2], "")
user = Player("user", 4, 4, [emptyweapon0, emptyobj0, emptyobj1], "")
players = {emptyplayer.name: emptyplayer, user.name: user, testplayer.name: testplayer}
castle = Loc(5, "castle")
# hmm = Player("hmm", 5, 10, True, [], poop, "apple", castle)
# smh = Player("smh", 5, 10, True, [], poop, "apple", castle)

# hmm.health()
# smh.attack(hmm)
# hmm.getLoc()
#testplayer.__init__(emptyplayer.name, emptyplayer.hp, emptyplayer.mhp, emptyplayer.inv, emptyplayer.loc)
# print("Is hmm living?", hmm.living)
print("You are standing in a field")


while True:
    cmd = input("> ")
    cmd = cmd.split(" ")
    if cmd[0].lower() in ("quit", "q", "exit"):
        break
    if cmd[0] == "attack":
        user.attack(players[cmd[1]])
    if cmd[0] == "health":
        if len(cmd) > 1:
            players[cmd[1]].health()
        else:
            user.health()
