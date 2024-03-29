import pandas as pd

from view.canvas import center_format, StatsCanvas

from game import player

# need to do import player due to circular import with player

STATS_FILE = 'stats/user_stats.csv'


class Statistics:

    user_stats = pd.read_csv(STATS_FILE)
    user_stats = user_stats.loc[:, ~user_stats.columns.str.contains('^Unnamed')]

    @staticmethod
    def get_user_stats(user: 'player.UserProfile') -> StatsCanvas:
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()
        return StatsCanvas(user_row)

    @staticmethod
    def lifetime_stats_to_string(user: 'player.UserProfile'):
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()

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
    def most_recent_game_stats_to_string(user: 'player.UserProfile'):
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == user.get_user_name()].squeeze()

        stats_string = center_format.format('YOUR RECENT GAME STATISTICS:') + \
            center_format.format('============================') + \
            center_format.format('Number of Hits: {}'.format(user_row.most_recent_game_hits)) + \
            center_format.format('Number of Hits Received: {}'.format(user_row.most_recent_game_hits_received)) + \
            center_format.format('Number of Misses: {}'.format(user_row.most_recent_game_misses)) + \
            center_format.format('Number of Misses Received: {}'.format(user_row.most_recent_game_misses_received)) + \
            center_format.format('Number of Ships Sunk: {}'.format(user_row.most_recent_game_ships_sunk)) + \
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

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name]

        if user_row.empty:
            return

        user_row.most_recent_game_hits = 0
        user_row.most_recent_game_hits_received = 0
        user_row.most_recent_game_misses = 0
        user_row.most_recent_game_misses_received = 0
        user_row.most_recent_game_ships_sunk = 0
        user_row.most_recent_game_ships_lost = 0

        Statistics.user_stats = Statistics.user_stats.loc[:, ~Statistics.user_stats.columns.str.contains('^Unnamed')]
        Statistics.user_stats.loc[Statistics.user_stats.user_name == name] = user_row
        Statistics.user_stats.to_csv('user_stats.csv')

    @staticmethod
    def update_stats(name: str, num_hits: int, num_misses: int, num_sunk: int, outgoing: bool):

        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name]

        if user_row.empty:
            return

        index = Statistics.get_row_index(name)
        if index == -1:
            return

        if outgoing:
            user_row.most_recent_game_hits += num_hits
            user_row.lifetime_hits += num_hits
            user_row.most_recent_game_misses += num_misses
            user_row.lifetime_misses += num_misses
            user_row.most_recent_game_ships_sunk += num_sunk
            user_row.lifetime_ships_sunk += num_sunk
        elif not outgoing:
            user_row.most_recent_game_hits_received += num_hits
            user_row.lifetime_hits_received += num_hits
            user_row.most_recent_game_misses_received += num_misses
            user_row.lifetime_misses_received += num_misses
            user_row.most_recent_game_ships_lost += num_sunk
            user_row.lifetime_ships_lost += num_sunk   

        Statistics.user_stats = Statistics.user_stats.loc[:, ~Statistics.user_stats.columns.str.contains('^Unnamed')]
        Statistics.user_stats.loc[Statistics.user_stats.user_name == name] = user_row
        Statistics.user_stats.to_csv('user_stats.csv')

    @staticmethod
    def update_win_loss_stats(name: str, won: bool):
        user_row = Statistics.user_stats.loc[Statistics.user_stats.user_name == name]

        if user_row.empty:
            return

        index = Statistics.get_row_index(name)
        if index == -1:
            return

        if won == True:
            user_row.lifetime_wins += 1
        else:
            user_row.lifetime_losses += 1

        Statistics.user_stats = Statistics.user_stats.loc[:, ~Statistics.user_stats.columns.str.contains('^Unnamed')]
        Statistics.user_stats.loc[Statistics.user_stats.user_name == name] = user_row
        Statistics.user_stats.to_csv('user_stats.csv')

    @staticmethod
    def create_user(user: 'player.UserProfile'):
        column_names = Statistics.user_stats.columns

        user_df = pd.DataFrame(0, columns=column_names, index=[0])
        user_df['user_name'] = user.user_name

        Statistics.user_stats = Statistics.user_stats.append(user_df)

        Statistics.user_stats = Statistics.user_stats.loc[:, ~Statistics.user_stats.columns.str.contains('^Unnamed')]
        # Statistics.user_stats.loc[Statistics.user_stats.user_name == name] = user_row
        Statistics.user_stats.to_csv('user_stats.csv')
