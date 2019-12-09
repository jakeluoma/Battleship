from typing import Optional

from game import Game
from statistics import Statistics
from player import UserProfile
from canvas import login_canvas, start_menu_canvas, MenuOption, exit_canvas, main_menu_canvas, StatsCanvas, \
    new_game_canvas, BoardCanvas, PlaceShipsMenuCanvas, FinishedPlacingShipsCanvas, TakeTurnCanvas
from view import View
import warnings

class Program:
    def __init__(self):
        self.known_users = list(Statistics.user_stats.user_name)
        self.ai_types = [0, 1]
        self.user = None
        self.game = None

    def login(self, view) -> MenuOption:
        user_name = view.get_username()
        user = UserProfile(user_name)
        self.user = user
        if user_name in self.known_users:
            pass
        else:
            Statistics.create_user(user)

        # returns next screen after logging in
        return MenuOption.MAINMENU

    def logout(self) -> MenuOption:
        self.user = None
        return MenuOption.STARTMENU

    def show_user_stats(self) -> StatsCanvas:
        return Statistics.get_user_stats(self.user)

    def create_new_game(self, view):
        self.game = Game(self.user, view)

    def noop(self):
        # This currently functions as a dummy function for program coordinator to call in it's run screen method when
        # there is no logic to be run by the program class. This currently happens for menu screens.
        pass

    def start_game(self) -> Optional[MenuOption]:
        return self.game.run_game()

    def load_game(self):
        try:
            self.game = Game.load_saved_game(self.user)
            return MenuOption.STARTGAME
        except:
            return

    def get_player_ship_placement_menu_canvas(self) -> PlaceShipsMenuCanvas:
        return self.game.get_player_ship_placement_canvas()

    def get_take_turn_canvas(self) -> TakeTurnCanvas:
        return self.game.get_take_turn_canvas()

    def place_ships(self):
        self.game.position_fleets()

    def exit(self):
        exit()


class ProgramAndViewCoordinator:
    option_canvas_map = {
        MenuOption.LOGIN: login_canvas,
        MenuOption.LOGOUT: start_menu_canvas,
        MenuOption.EXIT: exit_canvas,
        MenuOption.STARTMENU: start_menu_canvas,
        MenuOption.MAINMENU: main_menu_canvas,
        MenuOption.SHOWSTATS: lambda program: program.show_user_stats(),
        MenuOption.NEWGAMEMENU: new_game_canvas,
        MenuOption.PLACESHIPSMENU: lambda program: program.get_player_ship_placement_menu_canvas(),
        MenuOption.PLACESHIPS: None,
        MenuOption.STARTGAME: lambda program: program.get_take_turn_canvas(),
        MenuOption.LOADGAME: None
    }

    parameterized_with_program = [MenuOption.SHOWSTATS, MenuOption.PLACESHIPSMENU, MenuOption.STARTGAME]

    takes_view_argument = [MenuOption.LOGIN, MenuOption.NEWGAMEMENU]

    option_program_method_map = {
        MenuOption.STARTMENU: 'noop',
        MenuOption.MAINMENU: 'noop',
        MenuOption.PLACESHIPSMENU: 'noop',
        MenuOption.NEWGAMEMENU: 'create_new_game',
        MenuOption.LOGIN: 'login',
        MenuOption.LOGOUT: 'logout',
        MenuOption.SHOWSTATS: 'show_user_stats',
        MenuOption.EXIT: 'exit',
        MenuOption.PLACESHIPS: 'place_ships',
        MenuOption.STARTGAME: 'start_game',
        MenuOption.LOADGAME: 'load_game'
    }

    def __init__(self, program: Program, view: View):
        self.program = program
        self.view = view

    def run_screen(self, menu_option: MenuOption):
        """
        This is the driving function between the different game screens and corresponding program methods.
        The method takes in a menu option, that corresponds to a canvas screen. It accesses this canvas using the
        option_canvas_map and uses the view to paint this canvas. Then it gets the corresponding business logic
        associated with a given screen (executed by Program) from option_program_method_map, and calls it using getattr,
        the program object and the string name of the method to be called. Finally, it takes in the user's option for
        the next view to navigate to and calls itself with the new option, again repeating the process.
        Args:
            menu_option:

        Returns:

        """
        # Plain views vs Parameterized views
        if menu_option in self.parameterized_with_program:
            canvas = self.option_canvas_map[menu_option](self.program)
        else:
            canvas = self.option_canvas_map[menu_option]
        if canvas:
            self.view.update_display(canvas)
        args = [self.view] if menu_option in self.takes_view_argument else []
        next_menu = getattr(self.program, self.option_program_method_map[menu_option])(*args)
        if not isinstance(next_menu, MenuOption):
            next_menu = self.view.get_next_view()
        self.run_screen(next_menu)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    p, v = Program(), View()
    pc = ProgramAndViewCoordinator(p, v)
    pc.run_screen(MenuOption.STARTMENU)
