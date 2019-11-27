from typing import Tuple, Optional

from Coordinate import Coordinate
from PlayerLogic import Direction


class View:
    def get_input(self):
        pass

    def get_coordinate(self) -> Coordinate:
        inp = input()
        x, y = self.parse_coordinate(inp)
        return Coordinate(x, y)

    def get_direction(self) -> Direction:
        inp = input()
        dir = self.parse_direction(inp)
        return dir

    def parse_coordinate(self, inp) -> Optional[Tuple[int, int]]:
        x, y = None, None
        if len(inp) == 2:
            x, y = inp[0], inp[1]
        else:
            split = inp.split(",")
            if len(split) >= 2:
                x, y = split[0], split[1]
            else:
                split = inp.split(" ")
                if len(split) >= 2:
                    x, y = split[0], split[1]
        try:
            return int(x), int(y)
        except Exception:
            raise Exception("Invalid coordinates")

    def parse_direction(self, inp) -> Direction:
        if any(inp.startswith(k) for k in ["down", "go down", "below", "bottom", "s"]):
            return Direction.down
        elif any(inp.startswith(k) for k in ["up", "go up", "above", "top", "w"]):
            return Direction.up
        elif any(inp.startswith(k) for k in ["left", "go left", "a"]):
            return Direction.left
        elif any(inp.startswith(k) for k in ["right", "go right", "d"]):
            return Direction.right

        raise Exception("Invalid Direction")

view = View()
view.get_input()