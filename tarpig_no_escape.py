#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import traceback



#class Game:
#    def __init__(self, loc, move, file)


class Loc:
    def __init__(self, cord, name):
        self.cord = cord
        self.name = name


class Player:
    def __init__(self, name, hp, mhp, loc):
        self.name = name
        self.hp = hp
        self.mhp = mhp
        self.living = (self.hp > 0)
        self.inv = {}
        self.holding = None
        self.wearing = None
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
        healobj = None
        if isinstance(heal, Heal):
            if heal in self.inv.values():
                healObj = heal
            else:
                print(f"ERROR: @{self.name}: {heal.name} is not in your inventory.")
                return
        elif isinstance(heal, str):
            if heal in self.inv:
                healObj = self.inv[heal]
                if not isinstance(healObj, Heal):
                    print(f"ERROR: @{self.name}: {heal} is not a heal object in your inventory.")
                    return
            else:
                print("ERROR: @{self.name}: {heal} is not in your inventory.")
                return
        else:
            print("ERROR: @{self.name}: {heal} is not a heal in your inventory.")
            return

        self.setHP(self.hp + healObj.amount)
        print(f"@{self.name}: Healed. ", end="")
        self.health()


    def getinv(self):
        output = f"@{self.name}: Inventory:\n"
        for (k, v) in self.inv.items():
            if v == self.holding:
                output += " *" + k + "\n"
            elif x == self.wearing:
                output += "**" + k + "\n"
            else:
                output += "  " + k + "\n"
        print(output)

    def addinv(self, item):
        self.inv[item.name] = item

    def hold(self, item):
        self.holding = item

    def wear(self, item):
        self.wearing = item


    def attack(self, target):
        if isinstance(target, Player):
            if isinstance(self.holding, Weapon):
                target.setHP(target.hp-self.holding.dmg)
                print(f"@{self.name}: {target.name} took {self.holding.dmg} damage. ({str(target.hp)}/{str(target.mhp)})")
            else:
                print(f"ERROR: @{self.name}: {self.holding.name} is not a weapon.")
        else:
            print(f"ERROR: @{self.name}: {target.name} is not a person/animal")


class Item:
    def __init__(self, name, desc, owner):
        self.name = name
        self.desc = desc
        self.owner = owner
        self.owner.addinv(self)


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

def getTargetUser(cmd, players, user):
    if len(cmd) > 1:
        target = players[cmd[1]]
    else:
        target = user
    return target


def main():
    print("TaRPiG - Text Roleplaying game")
    emptyplayer = Player("emptyplayer", 3000, 3000, "")
    emptyobj0 = Item("empty0", "", emptyplayer)
    emptyobj1 = Item("empty1", "", emptyplayer)
    emptyobj2 = Item("empty2", "", emptyplayer)
    emptyobj3 = Item("empty3", "", emptyplayer)

    testplayer = Player("testplayer", 29, 30, "")
    user = Player("user", 4, 4,  "")
    emptyweapon0 = Weapon("emptyweapon0", "", user, 28)
    players = {emptyplayer.name: emptyplayer, user.name: user, testplayer.name: testplayer}
    user.hold(emptyweapon0)
    emptyplayer.hold(emptyobj0)
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
        try:
            cmd = input("> ")
            cmd = cmd.split(" ")
            if cmd[0].lower() in ("quit", "q", "exit"):
                break

            if cmd[0] == "attack":
                user.attack(getTargetUser(cmd, players, user))
            if cmd[0] == "health":
                getTargetUser(cmd, players, user).health()
            if cmd[0] == "heal":
                user.heal(cmd[1])
            if cmd[0] in ("inventory", "inv", "i"):
                user.getinv()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except:
            traceback.print_exc()
            continue

if __name__ == "__main__":
    import os
    import atexit
    import readline

    histfile = os.path.join(os.path.expanduser("~"), ".python_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)

    main()

