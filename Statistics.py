import pandas as pd


# note from Jake: it would be a lot cleaner if UserProfile had a reference to Statistics instead of Statistics to UserProfile.
# on init of statistics, it would make sense to generate an object that only contains the statistics relevant to that UserProfile.
# UserProfile would initialize Statistics during its own initialization.  Then it would be easy to update statistics during a Game
# by simply having UserProfile pass the update call to Statistics each turn.
# The way it's set up now almost requires Program to have a reference to Statistics and pass that reference down to Game, which passes
# it down to Player, etc.  Not very clean.
from player import UserProfile

STATS_FILE = 'user_stats.csv'


class Statistics:

    user_stats = pd.read_csv(STATS_FILE)

    @staticmethod
    def lifetime_stats_to_string(name: str):

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name].squeeze()

        stats_string = 'YOUR OVERALL STATISTICS:\n'
        stats_string += '==========================\n'
        stats_string += ('Number of Wins: {}\n'.format(user_row.lifetime_wins))
        stats_string += ('Number of Losses: {}\n'.format(user_row.lifetime_losses))
        stats_string += ('Number of Lifetime Hits: {}\n'.format(user_row.lifetime_hits))
        stats_string += ('Number of Lifetime Hits Received: {}\n'.format(user_row.lifetime_hits_received))
        stats_string += ('Number of Lifetime Misses: {}\n'.format(user_row.lifetime_misses))
        stats_string += ('Number of Lifetime Misses Received: {}\n'.format(user_row.lifetime_misses_received))
        stats_string += ('Number of Lifetime Ships Sunk: {}\n'.format(user_row.lifetime_ships_sunk))
        stats_string += ('Number of Lifetime Ships Lost: {}\n'.format(user_row.lifetime_ships_lost))

        return stats_string

    @staticmethod
    def most_recent_game_stats_to_string(name: str):

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name].squeeze()

        stats_string = 'YOUR RECENT GAME STATISTICS:\n'
        stats_string += '============================\n'
        stats_string += ('Number of Hits: {}\n'.format(user_row.most_recent_game_hits))
        stats_string += ('Number of Hits Received: {}\n'.format(user_row.most_recent_game_hits_received))
        stats_string += ('Number of Misses: {}\n'.format(user_row.most_recent_game_misses))
        stats_string += ('Number of Misses Received: {}\n'.format(user_row.most_recent_game_misses_received))
        stats_string += ('Number of Ships Sunk: {}\n'.format(user_row.most_recent_game_ships_sunk))
        stats_string += ('Number of Ships Lost: {}\n'.format(user_row.most_recent_game_ships_lost))

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

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name].squeeze()

        if user_row.empty:
            return

        # Change to self.row.property = 0?
        user_row.most_recent_game_hits = 0
        user_row.most_recent_game_hits_received = 0
        user_row.most_recent_game_misses = 0
        user_row.most_recent_game_misses_received = 0
        user_row.most_recent_game_ships_sunk = 0
        user_row.most_recent_game_ships_lost = 0

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
    def create_user(user: UserProfile):
        column_names = Statistics.user_stats.columns

        user_df = pd.DataFrame(0, columns=column_names, index=[0])
        user_df['user_name'] = user.user_name

        Statistics.user_stats = Statistics.user_stats.append(user_df)
        Statistics.user_stats.to_csv('user_stats.csv')
