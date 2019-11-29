import os
from enum import Enum
from typing import Tuple, Optional

from Coordinate import Coordinate
from board import Direction

center_format = "{0:^100}\n"


class MenuOption(Enum):
    STARTMENU = 0
    LOGIN = 1
    EXIT = 2
    STARTGAME = 3
    SHOWSTATS = 4


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


class MainMenuCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Main Menu xxxxxx") + \
            center_format.format("1. Play new game") + \
            center_format.format("2. Show User stats") + \
            center_format.format("3. Exit") + \
            center_format.format("Please select an option by typing one of the numbers above")

    def paint(self):
        print(self.display_string)


class StartMenuCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Start Menu xxxxxx") + \
            center_format.format("l: Login") + \
            center_format.format("x: Exit") + \
            center_format.format("Please select an option by typing one of the numbers above")

    def paint(self):
        print(self.display_string)

class ExitCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Exit Screen xxxxxx") + \
            center_format.format("You have exited the game. Goodbye!")

    def paint(self):
        print(self.display_string)


class InputParser:
    @staticmethod
    def parse_coordinate(inp) -> Optional[Tuple[int, int]]:
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

    @staticmethod
    def parse_direction(inp) -> Direction:
        if any(inp.lower().startswith(k) for k in ["down", "go down", "below", "bottom", "s"]):
            return Direction.down
        elif any(inp.lower().startswith(k) for k in ["up", "go up", "above", "top", "w"]):
            return Direction.up
        elif any(inp.lower().startswith(k) for k in ["left", "go left", "a"]):
            return Direction.left
        elif any(inp.lower().startswith(k) for k in ["right", "go right", "d"]):
            return Direction.right

        raise Exception("Invalid Direction")

    @staticmethod
    def parse_next_view(inp) -> MenuOption:
        if any(inp.lower().startswith(k) for k in ["l", "login"]):
            return MenuOption.LOGIN
        elif any(inp.lower().startswith(k) for k in ["e", "x", "exit"]):
            return MenuOption.EXIT
        elif any(inp.lower().startswith(k) for k in ["g", "start", "game"]):
            return MenuOption.STARTGAME
        elif any(inp.lower().startswith(k) for k in ["s", "stats", "show stats"]):
            return MenuOption.SHOWSTATS

        raise Exception("Invalid Option")


class View:
    def __init__(self):
        self.menu_option = None
        self.canvas = None

    def set_canvas(self, canvas: Canvas):
        self.canvas = canvas

    def set_menu_option(self, menu_option: MenuOption):
        self.menu_option = menu_option

    def clear_screen(self):
        os.system("cls")

    def update_display(self, canvas):
        self.clear_screen()
        self.set_menu_option(canvas_option_map[canvas])
        canvas.paint()

    def get_username(self):
        inp = input()
        return inp

    def get_coordinate(self) -> Coordinate:
        inp = input()
        x, y = InputParser.parse_coordinate(inp)
        return Coordinate(x, y)

    def get_direction(self) -> Direction:
        inp = input()
        return InputParser.parse_direction(inp)

    def get_next_view(self) -> MenuOption:
        inp = input()
        opt = InputParser.parse_next_view(inp)

        if opt not in valid_screen_transitions[self.menu_option]:
            raise Exception("You cannot use this option in this screen")

        return opt


login_canvas = LoginCanvas()
start_menu_canvas = StartMenuCanvas()
exit_canvas = ExitCanvas()

canvas_option_map = {
    login_canvas: MenuOption.LOGIN,
    exit_canvas: MenuOption.EXIT,
    start_menu_canvas: MenuOption.STARTMENU,
    # stats_canvas: MenuOption.SHOWSTATS
}

valid_screen_transitions = {
    MenuOption.STARTMENU: [MenuOption.LOGIN, MenuOption.EXIT],
}

# option_

if __name__ == "__main__":
    # l = LoginCanvas()
    # l.paint()
    v = View()
    v.display_canvas()