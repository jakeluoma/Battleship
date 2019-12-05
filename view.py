import os
from typing import Tuple, Optional

from Coordinate import Coordinate
from board import Direction
from canvas import Canvas, MenuOption, valid_screen_transitions, canvas_to_option


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
            return MenuOption.NEWGAMEMENU
        elif any(inp.lower().startswith(k) for k in ["s", "stats", "show stats"]):
            return MenuOption.SHOWSTATS
        elif any(inp.lower().startswith(k) for k in ["m", "menu", "main menu"]):
            return MenuOption.MAINMENU
        elif any(inp.lower().startswith(k) for k in ["p", "place", "ship"]):
            return MenuOption.PLACESHIPSMENU
        elif any(inp.lower().startswith(k) for k in ["c", "config", "display"]):
            return MenuOption.VIEWCONFIG
        elif any(inp.lower().startswith(k) for k in ["st", "start"]):
            return MenuOption.PLACESHIPS

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

    def update_display(self, canvas: Canvas):
        self.clear_screen()
        self.set_menu_option(canvas_to_option(canvas))
        canvas.paint()

    def update_canvas(self, *args):
        self.clear_screen()
        try:
            self.canvas.update(*args)
        except NotImplementedError:
            pass

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


