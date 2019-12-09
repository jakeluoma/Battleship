import os
from typing import Tuple, Optional, Union

from Coordinate import Coordinate
from board import Board, Direction
from canvas import Canvas, MenuOption, valid_screen_transitions, canvas_to_option
from settings import SettingsOption


class InputParser:
    @staticmethod
    def parse_coordinate(inp: str, board: Board) -> Optional[Tuple[int, int]]:
        row, col = None, None
        if len(inp) == 2:
            row, col = inp[0], inp[1]
        else:
            split = inp.split(",")
            if len(split) >= 2:
                row, col = split[0], split[1]
            else:
                split = inp.split(" ")
                if len(split) >= 2:
                    row, col = split[0], split[1]
        try:
            row, col = int(row), int(col)
            if row < 0 or col < 0 or row >= board.get_dimension() or col >= board.get_dimension():
                raise ValueError
            return row, col
        except:
            raise TypeError

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

        raise Exception("Invalid direction.  Try again.")

    @staticmethod
    def parse_next_view(inp, do_not_raise=False) -> Optional[MenuOption]:
        if any(inp.lower().startswith(k) for k in ["lo", "logout"]):
            return MenuOption.LOGOUT
        elif any(inp.lower().startswith(k) for k in ["lg", "load game"]):
            return MenuOption.LOADGAME
        elif any(inp.lower().startswith(k) for k in ["l", "login"]):
            return MenuOption.LOGIN
        elif any(inp.lower().startswith(k) for k in ["e", "x", "exit"]):
            return MenuOption.EXIT
        elif any(inp.lower().startswith(k) for k in ["g", "game"]):
            return MenuOption.NEWGAMEMENU
        elif any(inp.lower().startswith(k) for k in ["t", "start"]):
            return MenuOption.PLACESHIPS
        elif any(inp.lower().startswith(k) for k in ["s", "stats", "show stats"]):
            return MenuOption.SHOWSTATS
        elif any(inp.lower().startswith(k) for k in ["q", "m", "menu", "main menu"]):
            return MenuOption.MAINMENU
        elif any(inp.lower().startswith(k) for k in ["p", "place", "ship"]):
            return MenuOption.PLACESHIPSMENU
        elif any(inp.lower().startswith(k) for k in ["c", "config", "display"]):
            return MenuOption.VIEWCONFIG
        elif any(inp.lower().startswith(k) for k in ["n", "new", "a"]):
            return MenuOption.STARTGAME

        if do_not_raise:
            return

        raise Exception("Invalid selection.  Try again.")

    @staticmethod
    def parse_settings(inp) -> SettingsOption:
        if (inp in ['s', 'S', 'ship', 'Ship', 'SHIP']):
            return SettingsOption.CHANGE_SHIP_CELL
        elif (inp in ['h', 'H', 'hit', 'Hit', 'HIT']):
            return SettingsOption.CHANGE_HIT_CELL
        elif (inp in ['m', 'M', 'miss', 'Miss', 'MISS']):
            return SettingsOption.CHANGE_MISS_CELL
        else:
            return SettingsOption.NEW_GAME

# The View part of the MVC pattern
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
        self.canvas = canvas
        canvas.paint()

    def display_canvas(self):
        # self.clear_screen()
        self.canvas.paint()

    # def update_canvas(self, *args):
    #     self.clear_screen()
    #     try:
    #         self.canvas.update(*args)
    #         self.canvas.paint()
    #     except NotImplementedError:
    #         pass

    def get_username(self):
        inp = input()
        return inp

    def get_coordinate_or_quit(self, board: Board) -> Union[Coordinate, MenuOption]:
        while True:
            inp = input()
            try:
                opt = InputParser.parse_next_view(inp, do_not_raise=True)
                if not opt:
                    raise ValueError
                return opt
            except ValueError:
                try:
                    x, y = InputParser.parse_coordinate(inp, board)
                    return Coordinate(x, y)
                except ValueError:
                    print("Invalid coordinate given.  Try again.")
                except TypeError:
                    print("You must enter a coordinate (ie. 1,2).  Try again.")

    def get_direction(self) -> Direction:
        while True:
            inp = input()
            try:
                return InputParser.parse_direction(inp)
            except Exception as e:
                print(e.args[0])

    def get_next_view(self) -> MenuOption:
        while True:
            inp = input()
            try:
                opt = InputParser.parse_next_view(inp)
            except Exception as e:
                print(e.args[0])
                continue

            if opt not in valid_screen_transitions[self.menu_option]:
                print("You cannot use this option {} from this screen {}".format(opt.name, self.menu_option))
                continue

            return opt

    def get_yes_no(self):
        inp = input()
        return inp

    def get_char_choice(self):
        inp = input()
        return inp[0]


