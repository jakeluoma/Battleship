from player import UserProfile
import pandas as pd

# note from Jake: it would be a lot cleaner if UserProfile had a reference to Statistics instead of Statistics to UserProfile.
# on init of statistics, it would make sense to generate an object that only contains the statistics relevant to that UserProfile.
# UserProfile would initialize Statistics during its own initialization.  Then it would be easy to update statistics during a Game
# by simply having UserProfile pass the update call to Statistics each turn.
# The way it's set up now almost requires Program to have a reference to Statistics and pass that reference down to Game, which passes
# it down to Player, etc.  Not very clean.
class Statistics:

    user_stats = pd.read_csv('user_stats.csv')

    # def __init__(self):
    #     # self.row_name = user.get_user_name()
    #
    #     # self.row = self.user_stats.loc[self.user_stats.user_name == self.row_name]

    @staticmethod
    def lifetime_stats_to_string(name: str):

        row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name]

        stats_string = 'YOUR OVERALL STATISTICS:\n'
        stats_string += '==========================\n'
        stats_string += ('Number of Wins: ' + str(row.lifetime_wins) + '\n')
        stats_string += ('Number of Losses: ' + str(row.lifetime_losses) + '\n')
        stats_string += ('Number of Lifetime Hits: ' + str(row.lifetime_hits) + '\n')
        stats_string += ('Number of Lifetime Hits Received: ' + str(row.lifetime_hits_received) + '\n')
        stats_string += ('Number of Lifetime Misses: ' + str(row.lifetime_misses) + '\n')
        stats_string += ('Number of Lifetime Misses Received: ' + str(row.lifetime_misses_received) + '\n')
        stats_string += ('Number of Lifetime Ships Sunk: ' + str(row.lifetime_ships_sunk) + '\n')
        stats_string += ('Number of Lifetime Ships Lost: ' + str(row.lifetime_ships_lost) + '\n')

        return stats_string

    @staticmethod
    def most_recent_game_stats_to_string(name: str):

        row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name]

        stats_string = 'YOUR RECENT GAME STATISTICS:\n'
        stats_string += '============================\n'
        stats_string += ('Number of Hits: ' + str(row.most_recent_game_hits) + '\n')
        stats_string += ('Number of Hits Received: ' + str(row.most_recent_game_hits_received) + '\n')
        stats_string += ('Number of Misses: ' + str(row.most_recent_game_misses) + '\n')
        stats_string += ('Number of Misses Received: ' + str(row.most_recent_game_misses_received) + '\n')
        stats_string += ('Number of Ships Sunk: ' + str(row.most_recent_game_ships_sunk) + '\n')
        stats_string += ('Number of Ships Lost: ' + str(row.most_recent_game_ships_lost) + '\n')

        return stats_string

    @staticmethod
    def get_row_index(name: str):
        user_names = list(Statistics.user_stats.user_name)
        for i in range(len(user_names)):
            if user_names[i] == name:
                return i
        return -1


    @staticmethod
    def set_most_recent_game_stats_to_zero(name: str):

        index = Statistics.get_row_index(name)

        if index == -1:
            return

        # Change to self.row.property = 0?
        Statistics.user_stats.at[index, 'most_recent_game_hits'] = 0
        Statistics.user_stats.at[index, 'most_recent_game_hits_received'] = 0
        Statistics.user_stats.at[index, 'most_recent_game_misses'] = 0
        Statistics.user_stats.at[index, 'most_recent_game_misses_received'] = 0
        Statistics.user_stats.at[index, 'most_recent_game_ships_sunk'] = 0
        Statistics.user_stats.at[index, 'most_recent_game_ships_lost'] = 0

        Statistics.user_stats.to_csv('user_stats.csv')

    # updates the statistics for a single shot
    @staticmethod
    def update_stats(name: str, hit: bool, outgoing: bool, sunk: bool):

        index = Statistics.get_row_index(name)

        if index == -1:
            return

        if hit and outgoing:
            # Change to self.row.property += 1?
            Statistics.user_stats.at[index, 'most_recent_game_hits'] += 1
            Statistics.user_stats.at[index, 'lifetime_hits'] += 1
            if sunk:
                Statistics.user_stats.at[index, 'most_recent_game_ships_sunk'] += 1
                Statistics.user_stats.at[index, 'lifetime_ships_sunk'] += 1

        elif hit and not outgoing:
            Statistics.user_stats.at[index, 'most_recent_game_hits_received'] += 1
            Statistics.user_stats.at[index, 'lifetime_hits_received'] += 1
            if sunk:
                Statistics.user_stats.at[index, 'most_recent_game_ships_lost'] += 1
                Statistics.user_stats.at[index, 'lifetime_ships_lost'] += 1

        elif not hit and outgoing:
            Statistics.user_stats.at[index, 'most_recent_game_misses'] += 1
            Statistics.user_stats.at[index, 'lifetime_misses'] += 1

        elif not hit and not outgoing:
            Statistics.user_stats.at[index, 'most_recent_game_misses_received'] += 1
            Statistics.user_stats.at[index, 'lifetime_misses_received'] += 1

        Statistics.user_stats.to_csv('user_stats.csv')

    @staticmethod
    def create_user(user_df):
        Statistics.user_stats.append(user_df, ignore_index=True)
        Statistics.user_stats.to_csv('user_stats.csv')

