from enum import Enum

center_format = "{0:^100}\n"


class MenuOption(Enum):
    STARTMENU = 0
    LOGIN = 1
    EXIT = 2
    MAINMENU = 3
    NEWGAME = 4
    SHOWSTATS = 5


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
        self.display_string = center_format.format('YOUR OVERALL STATISTICS:') + \
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


login_canvas = LoginCanvas()
start_menu_canvas = StartMenuCanvas()
main_menu_canvas = MainMenuCanvas()
exit_canvas = ExitCanvas()


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

    raise Exception("No option found for canvas")


valid_screen_transitions = {
    MenuOption.STARTMENU: [MenuOption.LOGIN, MenuOption.EXIT],
    MenuOption.LOGIN: [MenuOption.MAINMENU],
    MenuOption.MAINMENU: [MenuOption.NEWGAME, MenuOption.SHOWSTATS, MenuOption.EXIT],
    MenuOption.SHOWSTATS: [MenuOption.MAINMENU]
}
