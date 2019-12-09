from abc import ABC
from typing import List

from components.tile import Coordinate
from view.options import MenuOption, CellConfig
from components.ship import ShipType, ship_size_map, Tile

# have to do "import settings" due to circular import with settings

center_format = "{0:^100}\n"


class Canvas(ABC):
    def __init__(self):
        self.view_width = 100

    def get_display_string(self):
        pass

    def paint(self):
        pass


class LoginCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Login xxxxxx") + \
            center_format.format("Please Enter your username")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class MainMenuCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Main Menu xxxxxx") + \
            center_format.format("lg: Load saved game") + \
            center_format.format("g: Play new game") + \
            center_format.format("s: Show User stats") + \
            center_format.format("lo: Logout") + \
            center_format.format("x: Exit") + \
            center_format.format("Please select an option by typing one of the characters above")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class StartMenuCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Start Menu xxxxxx") + \
            center_format.format("l: Login") + \
            center_format.format("x: Exit") + \
            center_format.format("Please select an option by typing one of the characters above")

    def get_display_string(self):
        return self.display_string

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

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class ExitCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Exit Screen xxxxxx") + \
            center_format.format("You have exited the game. Goodbye!")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class GameOverScreenCanvas(Canvas):
    def __init__(self, user_won=False):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Game Over xxxxxx") + \
            center_format.format("You won the game!!" if user_won else "Oh no! You lost the game :(") + \
            center_format.format("m: Back to main menu") + \
            center_format.format("x. Exit")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class NewGameCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxx Game Menu xxxxxx") + \
            center_format.format("p. Place ships") + \
            center_format.format("c. Configure display") + \
            center_format.format("m: Back to main menu") + \
            center_format.format("x. Exit") + \
            center_format.format("Please select an option by typing one of the characters above")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class BoardCanvas(Canvas):
    def __init__(self, board_dimension, is_target):
        self.board_dimension = board_dimension
        self.is_target = is_target
        self.board_coordinates_dict = {k: {} for k in range(self.board_dimension)}
        for key in self.board_coordinates_dict:
            self.board_coordinates_dict[key] = {k: CellConfig.empty_cell for k in range(self.board_dimension)}

        super().__init__()
        self.display_string = self.update(self.board_coordinates_dict)

    def get_display_string(self):
        return self.display_string

    def update(self, board_coordinates) -> str:
        display_string = center_format.format("xxxxxx {} Board xxxxxx".format("Opponent" if
                                                                              self.is_target else "Your")) + \
            center_format.format("\n\n") + \
            center_format.format("_|" + ("{}|"*self.board_dimension).format(*range(self.board_dimension)))
        for k in range(self.board_dimension):
            display_string += center_format.format("{}|".format(k) +
                                                   ("{}|"*self.board_dimension).format(*board_coordinates[k].values()))
        return display_string

    def update_hits(self, hits: List[Coordinate]) -> str:
        for coord in hits:
            self.board_coordinates_dict[coord.row][coord.column] = CellConfig.hit_cell
        self.display_string = self.update(self.board_coordinates_dict)
        return self.display_string

    def update_misses(self, misses: List[Coordinate]) -> str:
        for coord in misses:
            self.board_coordinates_dict[coord.row][coord.column] = CellConfig.missed_cell
        self.display_string = self.update(self.board_coordinates_dict)
        return self.display_string

    def update_ship_cells(self, ship_tiles: List[Tile]) -> str:
        for ship_tile in ship_tiles:
            coord = ship_tile.get_coordinate()
            self.board_coordinates_dict[coord.row][coord.column] = CellConfig.ship_cell
        self.display_string = self.update(self.board_coordinates_dict)
        return self.display_string

    def update_empty_cells(self, empty_cells: List[Coordinate]) -> str:
        for coord in empty_cells:
            self.board_coordinates_dict[coord.row][coord.column] = CellConfig.empty_cell
        self.display_string = self.update(self.board_coordinates_dict)
        return self.display_string

    def paint(self):
        print(self.display_string)


class PlaceShipsMenuCanvas(Canvas):
    def __init__(self, board_canvas: BoardCanvas):
        super().__init__()
        self.board_canvas = board_canvas
        self.display_string = self.board_canvas.get_display_string() + \
            center_format.format("\n\n") + \
            center_format.format("This is your current board.") + \
            center_format.format("t: Start placing ships") + \
            center_format.format("g: Back to game menu") + \
            center_format.format("x: Exit")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class PlaceShipsCanvas(Canvas):
    def __init__(self, board_canvas: BoardCanvas, ship_type: ShipType):
        super().__init__()
        self.board_canvas = board_canvas
        self.display_string = self.update(ship_type)

    def get_display_string(self):
        return self.display_string

    def update(self, ship: ShipType):
        return self.board_canvas.get_display_string() + center_format.format("\n\n") + \
            center_format.format("Enter the coordinates and direction of your ship.") + \
            center_format.format("Ship specification - "
                                 "Ship name: {} Ship Size: {}".format(ship.name, ship_size_map[ship])) + \
            center_format.format("Enter the coordinates on the first line, and the direction on the next") + \
            center_format.format("Coordinates specified by comma-separated numbers") + \
            center_format.format("Direction specified by the legend: w - up, a - left, d - right, s - down")

    def paint(self):
        print(self.display_string)


class FinishedPlacingShipsCanvas(Canvas):
    def __init__(self, board_canvas: BoardCanvas):
        super().__init__()
        self.board_canvas = board_canvas
        self.display_string = self.board_canvas.get_display_string() + \
            center_format.format("\n\n") + \
            center_format.format("You have finished placing all your ships!") + \
            center_format.format("n: Proceed to game") + \
            center_format.format("g: Start new game") + \
            center_format.format("x: Exit")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class TakeTurnCanvas(Canvas):
    def __init__(self, board_canvas: BoardCanvas, target_board_canvas: BoardCanvas, message=None, opponent_turn=False):
        super().__init__()
        self.board_canvas = board_canvas
        self.target_board_canvas = target_board_canvas
        self.opponent_turn = opponent_turn
        self.message = message
        self.display_string = self.update()

    def update(self) -> str:
        display_string = self.board_canvas.display_string + center_format.format("\n\n") + \
            self.target_board_canvas.display_string + \
            center_format.format("\n\n")

        if self.message:
            display_string += self.message + center_format.format("\n\n")

        if not self.opponent_turn:
            display_string += center_format.format("xxxxxx Make a move xxxxxx") + \
                center_format.format("q: quit game") + \
                center_format.format("Select a target for attack. ") + \
                center_format.format("Enter a coordinate - a row and column value separated by a comma like: 1,2")
        else:
            display_string += center_format.format("Waiting for Opponent's turn...")

        return display_string

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class ConfigureDisplayStartCanvas(Canvas):
    def __init__(self, message_canvas: Canvas = None):
        super().__init__()
        self.display_string = ""
        if message_canvas:
            self.display_string += message_canvas.get_display_string() + center_format.format("\n\n")
        self.display_string += center_format.format("Now you can configure display") + \
            center_format.format("\n\n") + \
            center_format.format("i: Change Ship Cell") + \
            center_format.format("j: Change Hit Cell") + \
            center_format.format("k: Change Miss Cell") + \
            center_format.format("g: Back to Game Menu")

    def get_display_string(self):
        return self.display_string

    def paint(self):
        print(self.display_string)


class EmptyCellChangeRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "Please Change the representation of empty cell: ")

    def paint(self):
        print(self.display_string)


class NotHitCellChangeRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "Please Change the representation of ship cell: ")

    def paint(self):
        print(self.display_string)


class HitCellChangeRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "Please Change the representation of hit cell: ")

    def paint(self):
        print(self.display_string)


class MissCellChangeRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "Please Change the representation of missed cell: ")

    def paint(self):
        print(self.display_string)


class EmptyCellChangedCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "===Empty cell representation updated successfully===") + \
            ConfigureDisplayStartCanvas().get_display_string()

    def paint(self):
        print(self.display_string)


class ShipCellChangedCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "===Ship cell representation updated successfully===") + \
            ConfigureDisplayStartCanvas().get_display_string()

    def paint(self):
        print(self.display_string)


class HitCellChangedCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "===Hit cell representation updated successfully===") + \
            ConfigureDisplayStartCanvas().get_display_string()

    def paint(self):
        print(self.display_string)


class MissCellChangedCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            "===Missed cell representation updated successfully===") + \
        ConfigureDisplayStartCanvas().get_display_string()

    def paint(self):
        print(self.display_string)


class CharacterEntryRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            " - Please enter character of your choice: ")

    def paint(self):
        print(self.display_string)


class EnterAgainRequestCanvas(Canvas):
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format(
            " - Please enter again: ")

    def paint(self):
        print(self.display_string)


login_canvas = LoginCanvas()
start_menu_canvas = StartMenuCanvas()
main_menu_canvas = MainMenuCanvas()
exit_canvas = ExitCanvas()
new_game_canvas = NewGameCanvas()

configure_display_start_canvas = ConfigureDisplayStartCanvas()
empty_cell_change_request_canvas = EmptyCellChangeRequestCanvas()
not_hit_cell_change_request_canvas = NotHitCellChangeRequestCanvas()
hit_cell_change_request_canvas = HitCellChangeRequestCanvas()
miss_cell_change_request_canvas = MissCellChangeRequestCanvas()
empty_cell_changed_canvas = EmptyCellChangedCanvas()
ship_cell_changed_canvas = ShipCellChangedCanvas()
hit_cell_changed_canvas = HitCellChangedCanvas()
miss_cell_changed_canvas = MissCellChangedCanvas()
character_entry_request_canvas = CharacterEntryRequestCanvas()
enter_again_request_canvas = EnterAgainRequestCanvas()


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
    elif isinstance(canvas, ConfigureDisplayStartCanvas):
        return MenuOption.VIEWCONFIG
    elif isinstance(canvas, NewGameCanvas):
        return MenuOption.NEWGAMEMENU
    elif isinstance(canvas, PlaceShipsMenuCanvas):
        return MenuOption.PLACESHIPSMENU
    elif isinstance(canvas, PlaceShipsCanvas):
        return MenuOption.PLACESHIPS
    elif isinstance(canvas, FinishedPlacingShipsCanvas):
        return MenuOption.FINISHEDPLACING
    elif isinstance(canvas, NotHitCellChangeRequestCanvas):
        return MenuOption.SHIPCELL
    elif isinstance(canvas, HitCellChangeRequestCanvas):
        return MenuOption.HITCELL
    elif isinstance(canvas, MissCellChangeRequestCanvas):
        return MenuOption.MISSCELL
    elif isinstance(canvas, TakeTurnCanvas):
        return MenuOption.STARTGAME
    elif isinstance(canvas, GameOverScreenCanvas):
        return MenuOption.GAMEOVER
    elif isinstance(canvas, CharacterEntryRequestCanvas):
        return MenuOption.CHARENTRY
    elif isinstance(canvas, ShipCellChangedCanvas):
        return MenuOption.SHIPCELLCHANGED
    elif isinstance(canvas, HitCellChangedCanvas):
        return MenuOption.HITCELLCHANGED
    elif isinstance(canvas, MissCellChangedCanvas):
        return MenuOption.MISSCELLCHANGED

    raise Exception("No option found for canvas: ", canvas.__class__.__name__)


valid_screen_transitions = {
    MenuOption.STARTMENU: [MenuOption.LOGIN, MenuOption.EXIT],
    MenuOption.LOGIN: [MenuOption.MAINMENU],
    MenuOption.LOGOUT: [MenuOption.STARTMENU],
    MenuOption.MAINMENU: [MenuOption.LOADGAME, MenuOption.NEWGAMEMENU, MenuOption.SHOWSTATS, MenuOption.LOGOUT, MenuOption.EXIT],
    MenuOption.LOADGAME: [MenuOption.STARTGAME],
    MenuOption.SHOWSTATS: [MenuOption.MAINMENU],
    MenuOption.NEWGAMEMENU: [MenuOption.PLACESHIPSMENU, MenuOption.VIEWCONFIG, MenuOption.MAINMENU, MenuOption.EXIT],
    MenuOption.PLACESHIPSMENU: [MenuOption.PLACESHIPS, MenuOption.STARTGAME, MenuOption.NEWGAMEMENU, MenuOption.EXIT],
    MenuOption.PLACESHIPS: [MenuOption.STARTGAME, MenuOption.NEWGAMEMENU, MenuOption.EXIT],
    MenuOption.FINISHEDPLACING: [MenuOption.STARTGAME, MenuOption.NEWGAMEMENU, MenuOption.EXIT],
    MenuOption.GAMEOVER: [MenuOption.MAINMENU, MenuOption.EXIT],
    MenuOption.STARTGAME: [MenuOption.MAINMENU, MenuOption.EXIT],
    MenuOption.VIEWCONFIG: [MenuOption.SHIPCELL, MenuOption.HITCELL, MenuOption.MISSCELL, MenuOption.NEWGAMEMENU],
    MenuOption.SHIPCELLCHANGED: [MenuOption.SHIPCELL, MenuOption.HITCELL, MenuOption.MISSCELL, MenuOption.NEWGAMEMENU],
    MenuOption.HITCELLCHANGED: [MenuOption.SHIPCELL, MenuOption.HITCELL, MenuOption.MISSCELL, MenuOption.NEWGAMEMENU],
    MenuOption.MISSCELLCHANGED: [MenuOption.SHIPCELL, MenuOption.HITCELL, MenuOption.MISSCELL, MenuOption.NEWGAMEMENU],
}
