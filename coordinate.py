from typing import Tuple

class Coordinate:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def get_row_and_column(self) -> Tuple[int, int]:
        return self.row, self.column