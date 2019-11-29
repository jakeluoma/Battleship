from Statistics import *
from view import View, login_canvas, start_menu_canvas, MenuOption, exit_canvas


class Program:
    def __init__(self):
        self.known_users = list(Statistics.user_stats.user_name)
        self.ai_types = [0, 1]
        self.view = View()

    def login(self):
        user_name = self.view.get_username()
        user = UserProfile(user_name)
        if user_name in self.known_users:
            pass
        else:
            Statistics.create_user(user)

        return user

    def show_user_stats(self, user: UserProfile):
        print(Statistics.lifetime_stats_to_string(user))
        print(Statistics.most_recent_game_stats_to_string(user))

    def start_menu(self):
        pass

    def start_game(self):
        pass

    def exit(self):
        exit()


class ProgramAndViewCoordinator:
    option_canvas_map = {
        MenuOption.LOGIN: login_canvas,
        MenuOption.EXIT: exit_canvas,
        MenuOption.STARTMENU: start_menu_canvas,
        # MenuOption.SHOWSTATS: stats_canvas
    }

    option_program_method_map = {
        MenuOption.STARTMENU: 'start_menu',
        MenuOption.LOGIN: 'login',
        MenuOption.SHOWSTATS: 'show_user_stats',
        MenuOption.EXIT: 'exit',
    }

    def __init__(self, program: Program, view: View):
        self.program = program
        self.view = view

    def run_screen(self, menu_option: MenuOption):
        self.view.update_display(self.option_canvas_map[menu_option])
        getattr(self.program, self.option_program_method_map[menu_option])()
        next_menu = self.view.get_next_view()
        self.run_screen(next_menu)


if __name__ == '__main__':
    p, v = Program(), View()
    pc = ProgramAndViewCoordinator(p, v)
    pc.run_screen(MenuOption.STARTMENU)
