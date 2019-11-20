

class Coordinate:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def getRowAndColumn(self) -> Tuple[int, int]:
        return self.row, self.column