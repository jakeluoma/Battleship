from typing import Tuple

class Coordinate:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def getRowAndColumn(self) -> Tuple[int, int]:
        return self.row, self.column