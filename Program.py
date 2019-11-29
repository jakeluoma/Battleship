import pandas as pd
from player import *
from Statistics import *


class Program:
    def __init__(self):
        self.known_users = list(Statistics.user_stats.user_name)
        self.ai_types = [0, 1]

    def login(self, user_name: str):
        user = UserProfile(user_name)
        if user_name in self.known_users:
            pass
        else:
            Statistics.create_user(user)

        return user

    def show_user_stats(self, user: UserProfile):
        name = user.get_user_name()
        print(Statistics.lifetime_stats_to_string(name))
        print(Statistics.most_recent_game_stats_to_string(name))

    def start_game(self):
        pass


if __name__ == '__main__':
    p = Program()
    puser = p.login("nikhil")
    p.show_user_stats(puser)