import pandas as pd

from player import UserProfile
from canvas import center_format, StatsCanvas

STATS_FILE = 'user_stats.csv'


class Statistics:

    user_stats = pd.read_csv(STATS_FILE)

    @staticmethod
    def get_user_stats(user: UserProfile) -> StatsCanvas:
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()
        return StatsCanvas(user_row)

    @staticmethod
    def lifetime_stats_to_string(user: UserProfile):
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()

        # Move this to StatsView
        stats_string = center_format.format('YOUR OVERALL STATISTICS:') + \
            center_format.format('==========================') + \
            center_format.format('Number of Wins: {}'.format(user_row.lifetime_wins)) + \
            center_format.format('Number of Losses: {}'.format(user_row.lifetime_losses)) + \
            center_format.format('Number of Lifetime Hits: {}'.format(user_row.lifetime_hits)) + \
            center_format.format('Number of Lifetime Hits Received: {}'.format(user_row.lifetime_hits_received)) + \
            center_format.format('Number of Lifetime Misses: {}'.format(user_row.lifetime_misses)) + \
            center_format.format('Number of Lifetime Misses Received: {}'.format(user_row.lifetime_misses_received)) + \
            center_format.format('Number of Lifetime Ships Sunk: {}'.format(user_row.lifetime_ships_sunk)) + \
            center_format.format('Number of Lifetime Ships Lost: {}'.format(user_row.lifetime_ships_lost))

        return stats_string

    @staticmethod
    def most_recent_game_stats_to_string(user: UserProfile):
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()

        # Move this to StatsView
        stats_string = center_format.format('YOUR RECENT GAME STATISTICS:') + \
            center_format.format('============================') + \
            center_format.format('Number of Hits: {}'.format(user_row.most_recent_game_hits)) + \
            center_format.format('Number of Hits Received: {}'.format(user_row.most_recent_game_hits_received)) + \
            center_format.format('Number of Misses Received: {}'.format(user_row.most_recent_game_misses_received)) + \
            center_format.format('Number of Ships Sunk: {}'.format(user_row.most_recent_game_ships_sunk)) + \
            center_format.format('Number of Misses: {}'.format(user_row.most_recent_game_misses)) + \
            center_format.format('Number of Ships Lost: {}'.format(user_row.most_recent_game_ships_lost))

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

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name].squeeze()

        if user_row.empty:
            return

        index = Statistics.get_row_index(name)

        if index == -1:
            return

        if hit and outgoing:
            user_row.most_recent_game_hits += 1
            user_row.lifetime_hits += 1
            if sunk:
                user_row.most_recent_game_ships_sunk += 1
                user_row.lifetime_ships_sunk += 1

        elif hit and not outgoing:
            user_row.most_recent_game_hits_received += 1
            user_row.lifetime_hits_received += 1
            if sunk:
                user_row.most_recent_game_ships_lost += 1
                user_row.lifetime_ships_lost += 1

        elif not hit and outgoing:
            user_row.most_recent_game_misses += 1
            user_row.lifetime_misses += 1

        elif not hit and not outgoing:
            user_row.most_recent_game_misses_received += 1
            user_row.lifetime_misses_received += 1

        Statistics.user_stats.to_csv('user_stats.csv')

    @staticmethod
    def create_user(user: UserProfile):
        column_names = Statistics.user_stats.columns

        user_df = pd.DataFrame(0, columns=column_names, index=[0])
        user_df['user_name'] = user.user_name

        Statistics.user_stats = Statistics.user_stats.append(user_df)
        Statistics.user_stats.to_csv('user_stats.csv')
