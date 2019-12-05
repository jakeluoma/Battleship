from enum import Enum

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
    def __init__(self):
        super().__init__()
        self.display_string = center_format.format("xxxxxx Your Board xxxxxx") + \
            center_format.format("\n\n") + \
            center_format.format("_|0|1|2|3|4|5|6|7|8|9|") + \
            center_format.format("0|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("1|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("2|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("3|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("4|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("5|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("6|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("7|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("8|_|_|_|_|_|_|_|_|_|_|") + \
            center_format.format("9|_|_|_|_|_|_|_|_|_|_|")

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
