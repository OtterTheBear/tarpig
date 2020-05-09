#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import traceback

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
        print(f"@{self.name}: HP: {output} {self.hp}/{self.mhp}" + " " + ("(Living)" if self.living else "(Dead)"))

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
                print(red + f"ERROR: @{self.name}: {heal.name} is not in your inventory." + reset)
                return
        elif isinstance(heal, str):
            if heal in self.inv:
                healObj = self.inv[heal]
                if not isinstance(healObj, Heal):
                    print(red + f"ERROR: @{self.name}: {heal} is not a heal object in your inventory." + reset)
                    return
            else:
                print(red + f"ERROR: @{self.name}: {heal} is not in your inventory." + reset)
                return
        else:
            print(red + f"ERROR: @{self.name}: {heal} is not a heal in your inventory." + reset)
            return

        self.setHP(self.hp + healObj.amount)
        print(f"@{self.name}: Healed. ", end="")
        self.health()

    def getinv(self):
        output = f"@{self.name}: Inventory:\n"
        for (k, v) in self.inv.items():
            if v == self.holding:
                output += " *" + k + "\n"
            elif v == self.wearing:
                output += "**" + k + "\n"
            else:
                output += "  " + k + "\n"
        return output

    def addinv(self, item):
        self.inv[item.name] = item


    def mvinv(self, target, item):
        itemobj = None
        if isinstance(item, Item):
            if item in self.inv.values():
                itemobj = item
            else:
                print(red + f"ERROR: @{self.name}: {item} is not in your inventory." + reset)
                return
        elif isinstance(item, str):
            if item in self.inv:
                itemobj = self.inv[item]
            else:
                print(red + f"ERROR: @{self.name}: {item} is not in your inventory." + reset)
                return
        else:
            print(red + f"ERROR: @{self.name}: {item} is not item." + reset)
            return
        target.inv[itemobj.name] = itemobj
        del self.inv[itemobj.name]

    def hold(self, item):
        if isinstance(item, Item):
            if item in self.inv.values():
                self.holding = item
            else:
                print(red + f"ERROR: @{user.name}: {item.name} is not in your inventory." + reset)
        else:
            print(red + f"ERROR: @{user.name}: {item.name} is not an item." + reset)

    def wear(self, item):
        self.wearing = item


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
    print("\x1b[2J\x1b[H")
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
            cmd = cmd.strip()
            cmd = cmd.split(" ")
            if cmd[0].lower() in ("quit", "q", "exit"):
                break

            elif cmd[0] == "attack":
                if len(cmd) > 1:
                    user.attack(getTargetUser(cmd, players, user))
                else:
                    raise IndexError
            elif cmd[0] == "health":
                getTargetUser(cmd, players, user).health()
            elif cmd[0] == "heal":
                user.heal(cmd[1])
            elif cmd[0] in ("inventory", "inv", "i"):
                print(user.getinv())
            elif cmd[0] == "hold":
                user.hold(cmd[1])
            elif cmd[0] == "gift":
                user.mvinv(getTargetUser(cmd, players, user), cmd[2])
            else:
                if cmd[0] != "":
                    print(red + f"ERROR: @{user.name}: \"{cmd[0]}\" is not a command." + reset)
            print(emptyplayer.getinv())
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except IndexError:
            print(red + f"ERROR: not enough arguments." + reset)
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

