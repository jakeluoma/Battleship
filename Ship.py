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


# class Carrier(Ship):
#     def __init__(self, tiles):
#         Ship.__init__(self, 'carrier', 5, tiles)
#
# class BattleShip(Ship):
#     def __init__(self, tiles):
#         Ship.__init__(self, 'battleship', 4, tiles)
#
# class Destroyer(Ship):
#     def __init__(self, tiles):
#         Ship.__init__(self, 'destroyer', 3, tiles)
#
# class Submarine(Ship):
#     def __init__(self, tiles):
#         Ship.__init__(self, 'submarine', 3, tiles)
#
# class PatrolBoat(Ship):
#     def __init__(self, tiles):
#         Ship.__init__(self, 'patrolboat', 2, tiles)

class ShipType(Enum):
    patrol_board = 0
    submarine = 1
    destroyer = 2
    battelship = 3
    carrier = 4


class ShipFactory:

    def __init__(self, ship_type_num):
        self.ship_type = ShipType(ship_type_num)
        self.ship_name = self.ship_type.name

    def makeShip(self, tiles):
        if self.ship_name == 'carrier':
            return Ship(self.ship_name, 5, tiles)
        elif self.ship_name == 'battleship':
            return Ship(self.ship_name, 4, tiles)
        elif self.ship_name == 'destroyer':
            return Ship(self.ship_name, 3, tiles)
        elif self.ship_name == 'submarine':
            return Ship(self.ship_name, 3, tiles)
        else:
            return Ship(self.ship_name, 2, tiles)

