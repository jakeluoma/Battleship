from typing import Tuple, Optional

from Coordinate import Coordinate
from board import Direction

center_format = "{0:^100}\n"


class Canvas:

    def __init__(self):
        self.view_width = 100

    def paint(self):
        pass


class LoginCanvas(Canvas):

    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Login xxxxxx") + \
            center_format.format("Please Enter your username")

    def paint(self):
        print(self.display_string)


class View:
    def __init__(self):
        self.canvas = None

    def set_canvas(self, canvas):
        self.canvas = canvas

    def display_canvas(self):
        self.canvas.paint()

    def get_username(self):
        inp = input()
        return inp

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


login_canvas = LoginCanvas()

if __name__ == "__main__":
    # l = LoginCanvas()
    # l.paint()
    v = View()
    v.display_canvas()