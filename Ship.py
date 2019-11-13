from abc import ABC
from Tile import *

# for now, no special attacks.  Let's just get the program working first.
class Ship:
    def __init__(self, name, size, tiles):
        if size != len(tiles):
            print("Size of ship " + name + " is " + size + " but it was assigned " + len(tiles) + " tiles")

        self.name = name
        self.size = size
        self.tiles = tiles

    def isSunk(self):
        sunk = True
        for tile in self.tiles:
            if tile.getHitStatus != TileHitStatus.HIT:
                sunk = False
                break
        return sunk


class Carrier(Ship):
    def __init__(self, tiles):
        Ship.__init__(self, 'carrier', 5, tiles)

class BattleShip(Ship):
    def __init__(self, tiles):
        Ship.__init__(self, 'battleship', 4, tiles)

class Destroyer(Ship):
    def __init__(self, tiles):
        Ship.__init__(self, 'destroyer', 3, tiles)

class Submarine(Ship):
    def __init__(self, tiles):
        Ship.__init__(self, 'submarine', 3, tiles)

class PatrolBoat(Ship):
    def __init__(self, tiles):
        Ship.__init__(self, 'patrolboat', 2, tiles)

class ShipType(Enum):
    patrol_board = 0
    submarine = 1
    destroyer = 2
    battelship = 3
    carrier = 4


class ShipFactory:
    pass