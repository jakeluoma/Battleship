import pandas as pd
from player import *
from Statistics import *


class Program:
    def __init__(self):
        self.user_stats = pd.read_csv('user_stats.csv')
        self.known_users =  list(self.user_stats.user_name)
        self.ai_types = [0, 1]

    def login(self, user_name: str):
        if user_name in self.known_users:
            pass
        else:
            user = UserProfile(user_name)
            user_df = user.set_stats_to_zero()
            self.user_stats.append(user_df, ignore_index= True)
            self.user_stats.to_csv('user_stats.csv')

    def show_user_stats(self, user: UserProfile):
        stats = Statistics(user)
        print(stats.lifetime_stats_to_string())
        print(stats.most_recent_game_stats_to_string())

    def start_game(self):
        pass

