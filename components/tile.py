from enum import Enum
from typing import Tuple


class Coordinate:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def get_row_and_column(self) -> Tuple[int, int]:
        return self.row, self.column


class TileHitStatus(Enum):
    EMPTY = 1
    HIT = 2
    MISS = 3


class Tile:
    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate
        self.ship = None
        self.hitStatus = TileHitStatus.EMPTY

    def get_coordinate(self) -> Coordinate:
        return self.coordinate

    def get_ship(self) -> 'Ship':
        return self.ship

    def get_hit_status(self) -> TileHitStatus:
        return self.hitStatus

    def set_ship(self, ship: 'Ship'):
        self.ship = ship

    def set_hit_status(self, hitStatus: TileHitStatus):
        self.hitStatus = hitStatus
