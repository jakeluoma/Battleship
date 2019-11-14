from player import UserProfile
import pandas as pd

class Statistics:
    def __init__(self, user: UserProfile):
        self.row_name = user.get_user_name()
        self.user_stats = pd.read_csv('user_stats.csv')
        self.row = self.user_stats.loc[self.user_stats.user_name == self.row_name]

    def lifetime_stats_to_string(self):

        stats_string = 'YOUR OVERALL STATISTICS:\n'
        stats_string += '==========================\n'
        stats_string += ('Number of Wins: ' + str(self.row.lifetime_wins) + '\n')
        stats_string += ('Number of Losses: ' + str(self.row.lifetime_losses) + '\n')
        stats_string += ('Number of Lifetime Hits: ' + str(self.row.lifetime_hits) + '\n')
        stats_string += ('Number of Lifetime Hits Received: ' + str(self.row.lifetime_hits_received) + '\n')
        stats_string += ('Number of Lifetime Misses: ' + str(self.row.lifetime_misses) + '\n')
        stats_string += ('Number of Lifetime Misses Received: ' + str(self.row.lifetime_misses_received) + '\n')
        stats_string += ('Number of Lifetime Ships Sunk: ' + str(self.row.lifetime_ships_sunk) + '\n')
        stats_string += ('Number of Lifetime Ships Lost: ' + str(self.row.lifetime_ships_lost) + '\n')

        return stats_string


    def most_recent_game_stats_to_string(self):

        stats_string = 'YOUR RECENT GAME STATISTICS:\n'
        stats_string += '============================\n'
        stats_string += ('Number of Hits: ' + str(self.row.most_recent_game_hits) + '\n')
        stats_string += ('Number of Hits Received: ' + str(self.row.most_recent_game_hits_received) + '\n')
        stats_string += ('Number of Misses: ' + str(self.row.most_recent_game_misses) + '\n')
        stats_string += ('Number of Misses Received: ' + str(self.row.most_recent_game_misses_received) + '\n')
        stats_string += ('Number of Ships Sunk: ' + str(self.row.most_recent_game_ships_sunk) + '\n')
        stats_string += ('Number of Ships Lost: ' + str(self.row.most_recent_game_ships_lost) + '\n')

        return stats_string

    def get_row_index(self):
        user_names = list(self.user_stats.user_name)
        for i in range(len(user_names)):
            if user_names[i] == self.row_name:
                return i
        return -1

    def set_most_recent_game_stats_to_zero(self):

        index = self.get_row_index()

        if index == -1:
            return

        self.user_stats.at[index, 'most_recent_game_hits'] = 0
        self.user_stats.at[index, 'most_recent_game_hits_received'] = 0
        self.user_stats.at[index, 'most_recent_game_misses'] = 0
        self.user_stats.at[index, 'most_recent_game_misses_received'] = 0
        self.user_stats.at[index, 'most_recent_game_ships_sunk'] = 0
        self.user_stats.at[index, 'most_recent_game_ships_lost'] = 0

        self.user_stats.to_csv('user_stats.csv')

    def update_stats(self, hit, outgoing, sunk):

        index = self.get_row_index()

        if hit:
            self.user_stats.at[index, 'lifetime_hits'] += 1

        if outgoing and not hit:
            self.user_stats.at[index, 'lifetime_misses'] += 1

        if sunk:
            self.user_stats.at[index, 'lifetime_ships_sunk'] += 1

        self.user_stats.to_csv('user_stats.csv')

