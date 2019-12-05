from statistics import Statistics
from player import UserProfile
from canvas import login_canvas, start_menu_canvas, MenuOption, exit_canvas, main_menu_canvas, StatsCanvas, \
    new_game_canvas
from view import View


class Program:
    def __init__(self):
        self.known_users = list(Statistics.user_stats.user_name)
        self.ai_types = [0, 1]
        self.view = View()
        self.user = None

    def login(self) -> MenuOption:
        user_name = self.view.get_username()
        user = UserProfile(user_name)
        self.user = user
        if user_name in self.known_users:
            pass
        else:
            Statistics.create_user(user)

        # returns next screen after logging in
        return MenuOption.MAINMENU

    def show_user_stats(self) -> StatsCanvas:
        return Statistics.get_user_stats(self.user)

    def start_menu(self):
        #TODO
        pass

    def noop(self):
        # This currently functions as a dummy function for program coordinator to call in it's run screen method when
        # there is no logic to be run by the program class. This currently happens for menu screens.
        pass

    def exit(self):
        exit()


class ProgramAndViewCoordinator:
    option_canvas_map = {
        MenuOption.LOGIN: login_canvas,
        MenuOption.EXIT: exit_canvas,
        MenuOption.STARTMENU: start_menu_canvas,
        MenuOption.MAINMENU: main_menu_canvas,
        MenuOption.SHOWSTATS: lambda program: program.show_user_stats(),
        MenuOption.NEWGAMEMENU: new_game_canvas,
    }

    parameterized_with_program = [MenuOption.SHOWSTATS]

    option_program_method_map = {
        MenuOption.STARTMENU: 'noop',
        MenuOption.MAINMENU: 'noop',
        MenuOption.NEWGAMEMENU: 'noop',
        MenuOption.LOGIN: 'login',
        MenuOption.SHOWSTATS: 'show_user_stats',
        MenuOption.EXIT: 'exit',
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
        self.view.update_display(canvas)
        next_menu = getattr(self.program, self.option_program_method_map[menu_option])()
        if not isinstance(next_menu, MenuOption):
            next_menu = self.view.get_next_view()
        self.run_screen(next_menu)


if __name__ == '__main__':
    p, v = Program(), View()
    pc = ProgramAndViewCoordinator(p, v)
    pc.run_screen(MenuOption.STARTMENU)
