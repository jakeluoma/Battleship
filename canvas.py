from enum import Enum
from typing import List

from Coordinate import Coordinate
from settings import Settings

center_format = "{0:^100}\n"


class MenuOption(Enum):
    STARTMENU = 0
    LOGIN = 1
    EXIT = 2
    MAINMENU = 3
    NEWGAMEMENU = 4
    SHOWSTATS = 5
    PLACESHIPS = 6
    VIEWCONFIG = 7


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
            center_format.format("g. Play new game") + \
            center_format.format("s. Show User stats") + \
            center_format.format("x. Exit") + \
            center_format.format("Please select an option by typing one of the characters above")

    def paint(self):
        print(self.display_string)


class StartMenuCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Start Menu xxxxxx") + \
            center_format.format("l: Login") + \
            center_format.format("x: Exit") + \
            center_format.format("Please select an option by typing one of the characters above")

    def paint(self):
        print(self.display_string)


class StatsCanvas(Canvas):
    def __init__(self, user_row: 'pandas.Dataframe'):
        super().__init__()
        self.display_string = center_format.format('xxxxxx YOUR OVERALL STATISTICS xxxxxx') + \
            center_format.format('==========================') + \
            center_format.format('Number of Wins: {}'.format(user_row.lifetime_wins)) + \
            center_format.format('Number of Losses: {}'.format(user_row.lifetime_losses)) + \
            center_format.format('Number of Lifetime Hits: {}'.format(user_row.lifetime_hits)) + \
            center_format.format('Number of Lifetime Hits Received: {}'.format(user_row.lifetime_hits_received)) + \
            center_format.format('Number of Lifetime Misses: {}'.format(user_row.lifetime_misses)) + \
            center_format.format('Number of Lifetime Misses Received: {}'.format(user_row.lifetime_misses_received)) + \
            center_format.format('Number of Lifetime Ships Sunk: {}'.format(user_row.lifetime_ships_sunk)) + \
            center_format.format('Number of Lifetime Ships Lost: {}'.format(user_row.lifetime_ships_lost)) + \
            center_format.format("\n\n") + \
            center_format.format('YOUR RECENT GAME STATISTICS:') + \
            center_format.format('============================') + \
            center_format.format('Number of Hits: {}'.format(user_row.most_recent_game_hits)) + \
            center_format.format('Number of Hits Received: {}'.format(user_row.most_recent_game_hits_received)) + \
            center_format.format('Number of Misses Received: {}'.format(user_row.most_recent_game_misses_received)) + \
            center_format.format('Number of Ships Sunk: {}'.format(user_row.most_recent_game_ships_sunk)) + \
            center_format.format('Number of Misses: {}'.format(user_row.most_recent_game_misses)) + \
            center_format.format('Number of Ships Lost: {}'.format(user_row.most_recent_game_ships_lost)) + \
            center_format.format("\n") + \
            center_format.format("m: Back to main menu")

    def paint(self):
        print(self.display_string)


class ExitCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Exit Screen xxxxxx") + \
            center_format.format("You have exited the game. Goodbye!")

    def paint(self):
        print(self.display_string)


class NewGameCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxx Game Menu xxxxxx") + \
            center_format.format("p. Place ships") + \
            center_format.format("c. Configure display") + \
            center_format.format("x. Exit")

    def paint(self):
        print(self.display_string)


class BoardCanvas(Canvas):
    def __init__(self, is_target):
        self.is_target = is_target
        self.board_coordinates_dict = {k: {} for k in range(10)}
        for key in self.board_coordinates_dict:
            self.board_coordinates_dict[key] = {k: Settings.empty_cell for k in range(10)}

        super().__init__()
        self.display_string = self.update_display(self.board_coordinates_dict)

    def update_display(self, board_coordinates) -> str:
        return center_format.format("xxxxxx {} Board xxxxxx".format("Opponent" if self.is_target else "Your")) + \
            center_format.format("\n\n") + \
            center_format.format("_|0|1|2|3|4|5|6|7|8|9|") + \
            center_format.format("0|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[0].values())) + \
            center_format.format("1|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[1].values())) + \
            center_format.format("2|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[2].values())) + \
            center_format.format("3|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[3].values())) + \
            center_format.format("4|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[4].values())) + \
            center_format.format("5|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[5].values())) + \
            center_format.format("6|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[6].values())) + \
            center_format.format("7|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[7].values())) + \
            center_format.format("8|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[8].values())) + \
            center_format.format("9|{}|{}|{}|{}|{}|{}|{}|{}|{}}|{}|".format(*board_coordinates[9].values()))

    def update_hits(self, hits: List[Coordinate]) -> str:
        for row, col in hits:
            self.board_coordinates_dict[row][col] = Settings.hit_cell
        return self.update_display(self.board_coordinates_dict)

    def update_misses(self, misses: List[Coordinate]) -> str:
        for row, col in misses:
            self.board_coordinates_dict[row][col] = Settings.missed_cell
        return self.update_display(self.board_coordinates_dict)

    def update_ship_cells(self, ship_cells: List[Coordinate]) -> str:
        for row, col in ship_cells:
            self.board_coordinates_dict[row][col] = Settings.ship_cell
        return self.update_display(self.board_coordinates_dict)

    def update_empty_cells(self, empty_cells: List[Coordinate]) -> str:
        for row, col in empty_cells:
            self.board_coordinates_dict[row][col] = Settings.empty_cell
        return self.update_display(self.board_coordinates_dict)

    def paint(self):
        print(self.display_string)


login_canvas = LoginCanvas()
start_menu_canvas = StartMenuCanvas()
main_menu_canvas = MainMenuCanvas()
exit_canvas = ExitCanvas()
new_game_canvas = NewGameCanvas()


def canvas_to_option(canvas: Canvas):
    if isinstance(canvas, LoginCanvas):
        return MenuOption.LOGIN
    elif isinstance(canvas, ExitCanvas):
        return MenuOption.EXIT
    elif isinstance(canvas, StartMenuCanvas):
        return MenuOption.STARTMENU
    elif isinstance(canvas, MainMenuCanvas):
        return MenuOption.MAINMENU
    elif isinstance(canvas, StatsCanvas):
        return MenuOption.SHOWSTATS
    elif isinstance(canvas, NewGameCanvas):
        return MenuOption.NEWGAMEMENU

    raise Exception("No option found for canvas")


valid_screen_transitions = {
    MenuOption.STARTMENU: [MenuOption.LOGIN, MenuOption.EXIT],
    MenuOption.LOGIN: [MenuOption.MAINMENU],
    MenuOption.MAINMENU: [MenuOption.NEWGAMEMENU, MenuOption.SHOWSTATS, MenuOption.EXIT],
    MenuOption.SHOWSTATS: [MenuOption.MAINMENU],
    MenuOption.NEWGAMEMENU: [MenuOption.PLACESHIPS, MenuOption.VIEWCONFIG, MenuOption.EXIT]
}
