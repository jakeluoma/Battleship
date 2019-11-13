from Ship import *

class ShipFactory:

    def makeShip(self, ship_type, tiles):
        if ship_type == 'carrier':
            return Carrier(tiles)
        elif ship_type == 'battleship':
            return BattleShip(tiles)
        elif ship_type == 'destroyer':
            return Destroyer(tiles)
        elif ship_type == 'submarine':
            return Submarine(tiles)
        else:
            return PatrolBoat(tiles)
