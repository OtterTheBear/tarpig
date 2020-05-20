#! /usr/bin/python3
# This is just a bunch of class definitions... for now
import traceback

red = "\x1b[1;31m"
green = "\x1b[1;92m"
reset = "\x1b[1;0m"

#class Game:
#    def __init__(self, loc, move, file)



class Loc:
    def __init__(self, cord, name, desc):
        self.cord = cord
        self.name = name
        self.desc = desc
        self.players = {}
        self.items = {}

    def addplayer(self, player):
        self.players[player.name] = player

    def mvplayer(self, target, player):
        target.players[player.name] = self.players[player]
        del self.players[player.name]
    
    def additem(self, item, player):
        itemobj = None
        if isinstance(item, Item):
            self.items[item.name] = player.inv[item.name]
        elif isinstance(item, str):
            self.items[item] = player.inv[item]
        else:
            print("err")
            return

    def mvitem(self, target, item):
        target.items[item.name] = self.items[item]
        del self.items[item.name]

    def getplayers(self):
        for x in self.players.values():
            print(x.name)

    def fulldesc(self):
        output = "Location: " + self.name + "\nDescription: " + self.desc + "\nItems:\n"
        if len(self.items) == 0:
            output += "  (None)\n"
        else:
            for x in self.items.values():
                output += "  " + x.name + "\n"

        output += "Players:\n"

        if len(self.players) == 0:
            output += "  (None)\n"
        else:
            for x in self.players.values():
                output += "  " + x.name + " " +  ("(Living)" if x.living else "(Dead)") + "\n"
            return output


class Player:
    def __init__(self, name, hp, mhp, loc):
        self.name = name
        self.hp = hp
        self.mhp = mhp
        self.living = (self.hp > 0)
        self.inv = {}
        self.holding = None
        self.wearing = None
        self.gold = 0
        self.loc = loc
        self.loc.addplayer(self)

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

    def drop(self, item):
        itemobj = None
        if isinstance(item, Item):
            itemobj = self.inv[item.name]
        elif isinstance(item, str):
            itemobj = self.inv[item]

        if itemobj == self.holding:
            self.holding = None
        if itemobj == self.wearing:
            self.wearing == None
        self.loc.additem(itemobj.name, self)
        del self.inv[itemobj.name]

    def grab(self, item):
        itemobj = None
        if isinstance(item, Item):
            itemobj = self.loc.items[item.name]
        elif isinstance(item, str):
            itemobj = self.loc.items[item]
        else:
            return
        self.inv[itemobj.name] = itemobj
        del self.loc.items[itemobj.name]

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
                output += " *" + v.name + v.desc + "\n"
            elif v == self.wearing:
                output += "**" + v.name + v.desc + "\n"
            else:
                output += "  " + v.name + v.desc + "\n"
        output += f"Gold: {self.gold}\n"
        return output

    def addinv(self, item):
        if isinstance(item, Item):
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
            print(red + f"ERROR: @{self.name}: {item} is not an item." + reset)
            return
        self.holding = itemobj

    def wear(self, item):
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
            print(red + f"ERROR: @{self.name}: {item} is not an item." + reset)
            return
        self.wearing = itemobj
    
    def addgold(self, amount):
        if self.gold + amount < 0:
            print(red + f"ERROR: @{self.name}: Not enough money." + reset)
        else:
            self.gold += amount

    def pay(self, target, amount):
        target.addgold(amount)
        self.addgold(-amount)

    def attack(self, target):
        targetsArmourStrength = (0 if target.wearing == None else target.wearing.strength)
        if isinstance(target, Player):
            if isinstance(self.holding, Weapon):
                effectivedmg =  self.holding.dmg - targetsArmourStrength
                if effectivedmg < 0:
                    effectivedmg = 0
                    target.setHP(target.hp)
                else:
                    target.setHP(target.hp-effectivedmg)
                print(f"@{self.name}: {target.name} took {effectivedmg} damage. ({str(target.hp)}/{str(target.mhp)})")
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
        if self.desc != "":
            self.desc = f" -- +{self.amount} HP ({self.count}) -- " + self.desc


class Weapon(Item):
    def __init__(self, name, desc, owner, dmg):
        Item.__init__(self, name, desc, owner)
        self.dmg = dmg
        if self.desc != "":
            self.desc = f" -- {self.dmg} DMG -- " + self.desc
        else:
            self.desc = f" -- {self.dmg} DMG"


class Armour(Item):
    def __init__(self, name, desc, owner, strength):
        Item.__init__(self, name, desc, owner)
        self.strength = strength
        if self.desc != "":
            self.desc = f"-{self.strength} DMG -- " + self.desc


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
    field = Loc(0, "Field", "a location")
    emptyplayer = Player("emptyplayer", 30, 3000, field)
    emptyobj0 = Item("empty0", "", emptyplayer)
    emptyobj1 = Item("empty1", "", emptyplayer)
    emptyobj2 = Item("empty2", "", emptyplayer)
    emptyobj3 = Item("empty3", "", emptyplayer)
    emptyarm0 = Armour("emptyarm0", "", emptyplayer, 11)

    testplayer = Player("testplayer", 29, 30, field)
    user = Player("user", 4, 4,  field)
    emptyweapon0 = Weapon("emptyweapon0", "an emptyweapon", user, 10)
    emptyweapon1 = Weapon("emptyweapon1", "", user, 201)
    emptyheal0 = Heal("emptyheal0", "", user, 1)
    emptyheal1 = Heal("emptyheal1", "", user, 1)
    players = {emptyplayer.name: emptyplayer, user.name: user, testplayer.name: testplayer}
    user.hold(emptyweapon0)
    emptyplayer.hold(emptyobj0)
    emptyplayer.wear(emptyarm0)
    ###############castle = Loc(5, "castle")
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
            if cmd.strip() == "":
                continue
            else:
                cmd = cmd.strip()
                cmd = cmd.split()
            if cmd[0].lower() in ("quit", "q", "exit"):
                break

            elif cmd[0] == "attack":
                if len(cmd) > 1:
                    user.attack(getTargetUser(cmd, players, user))
                else:
                    raise IndexError
            elif cmd[0] in ("h", "health"):
                getTargetUser(cmd, players, user).health()
            elif cmd[0] == "heal":
                user.heal(cmd[1])
            elif cmd[0] in ("inventory", "inv", "i"):
                print(user.getinv(), end="")
            elif cmd[0] == "hold":
                user.hold(cmd[1])
            elif cmd[0] == "wear":
                user.wear(cmd[1])
            elif cmd[0] == "gift":
                user.mvinv(getTargetUser(cmd, players, user), cmd[2])
            elif cmd[0] == "\x24\x24":
                for x in range(9):
                    getTargetUser(cmd, players, user).gold += 9
            elif cmd[0] in ("l", "location", "loc"):
                print(user.loc.fulldesc())
            elif cmd[0] in ("d", "drop"):
                user.drop(cmd[1])
            elif cmd[0] in ("g", "grab"):
                user.grab(cmd[1])
            else:
                if cmd[0] != "":
                    print(red + f"ERROR: @{user.name}: \"{cmd[0]}\" is not a command." + reset)
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

