import os
import pickle
from time import sleep
from typing import List, Optional

from stats import statistics
from view.options import MenuOption
from game.player_logic import CommandLineInstruction, AI
from components.ship import ShipType
from components.board import Board
from view.canvas import PlaceShipsMenuCanvas, PlaceShipsCanvas, FinishedPlacingShipsCanvas, TakeTurnCanvas, center_format, \
    GameOverScreenCanvas
from game.player import Player, UserProfile
from view.view import View


class GameMode:
    def __init__(self):
        self.board_dimension = 5
        self.ship_types: List[ShipType] = [ShipType.SUBMARINE, ShipType.SUBMARINE, ShipType.SUBMARINE]

    def get_dimension(self) -> int:
        return self.board_dimension

    def get_ship_types(self) -> List[ShipType]:
        return self.ship_types


class Game:
    def __init__(self, user_profile: UserProfile, view: View, game_mode: GameMode = GameMode()):
        # initialize human player
        fleet_board = Board(game_mode.get_dimension(), is_target=False)
        target_board = Board(game_mode.get_dimension(), is_target=True)
        self.player1 = Player(user_profile, CommandLineInstruction(), fleet_board, target_board,
                              game_mode.get_ship_types(), is_ai=False)
        statistics.Statistics.set_most_recent_game_stats_to_zero(self.player1.user_profile.get_user_name())

        # initialize AI player
        fleet_board = Board(game_mode.get_dimension(), is_target=False)
        target_board = Board(game_mode.get_dimension(), is_target=True)
        self.player2 = Player(None, AI(), fleet_board, target_board, game_mode.get_ship_types(), is_ai=True)

        # set each Player's opponent to finish Player initialization
        self.player1.setOpponent(self.player2)
        self.player2.setOpponent(self.player1)

        # human player will start first
        self.current_player = self.player2

        # Game implements the Model part of the MVC pattern
        self.view = view

    # Switch the current player
    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Alternates between players' turns. Continues loop as long as no player has achieved victory
    def run_game(self, dry_run=False) -> Optional[MenuOption]:
        # dry_run=True
        if dry_run:
            self.player2.victory = True
            self.end_game()
            return
        
        while not self.current_player.is_victorious():
            self.save_game() # the game is saved after every turn
            self.switch_player()
            ret = self.current_player.take_turn()
            if isinstance(ret, MenuOption):
                return ret
            hits, misses, ships_lost = ret

            message = ""
            if self.current_player == self.player1:
                self.player1.target_board.canvas.update_hits(hits)
                self.player1.target_board.canvas.update_misses(misses)
                if hits:
                    message += center_format.format("Your attack on the coordinates: "
                                                    "{} resulted in successful hits\n".format
                                                    ([(h.row, h.column) for h in hits]))
                if misses:
                    message += center_format.format("Your attack on the coordinates: "
                                                    "{} unfortunately missed the target\n".format
                                                    ([(m.row, m.column) for m in misses]))

                if ships_lost:
                    message += center_format.format("You just sunk these ships!: {}".format
                                                    (([(ship.name, ship.get_size()) for ship in ships_lost]))) + \
                        center_format.format("Your opponent has the following ships remaining: {}".format
                                             ([(ship.name, ship.get_size()) for ship in self.player2.fleet]))

                opponent_turn = True
            else:
                self.player1.fleet_board.canvas.update_hits(hits)
                self.player1.fleet_board.canvas.update_misses(misses)
                if hits:
                    message += center_format.format("Your opponent's attack on the coordinates: "
                                                    "{} resulted in successful hits\n".format
                                                    ([(h.row, h.column) for h in hits]))
                if misses:
                    message += center_format.format("Your opponent's attack on the coordinates: "
                                                    "{} missed the target\n".format
                                                    ([(m.row, m.column) for m in misses]))
                if ships_lost:
                    message += center_format.format("Your opponent just sunk these ships!: {}".format
                                                    ([(ship.name, ship.get_size()) for ship in ships_lost])) + \
                        center_format.format("You have the following ships remaining: {}".format
                                             ([(ship.name, ship.get_size()) for ship in self.player1.fleet]))
                opponent_turn = False

            self.view.update_display(TakeTurnCanvas(self.player1.fleet_board.canvas,
                                                    self.player1.target_board.canvas, message, opponent_turn))
            sleep(2)

        self.end_game()

    # Prints Victory or Loss screen and ends game
    def end_game(self):
        user_won = False
        if self.player1.is_victorious():
            user_won = True
        statistics.Statistics.update_win_loss_stats(self.player1.user_profile.get_user_name(), user_won)
        self.delete_game()
        self.view.update_display(GameOverScreenCanvas(user_won=user_won))

    # saves game to pickle, which gets written to file
    # the pickle files implicitly implment the Memento pattern with
    # Program and Game
    def save_game(self):
        # player1 is the human user
        relative_file_path = "save_game_" + self.player1.user_profile.get_user_name() + ".p"
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, "saves", relative_file_path)
        try:
            pickle.dump(self, open(file_path, "wb"))
        except:
            print("Failed to save game")

    def delete_game(self):
        # player1 is the human user
        relative_file_path = "save_game_" + self.player1.user_profile.get_user_name() + ".p"
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, "saves", relative_file_path)
        try:
            os.remove(relative_file_path)
        except OSError:
            pass

    # intended to be called by a non-Game instance.  Loads a saved game from a pickle
    # and returns a Game instance.
    @staticmethod
    def load_saved_game(user: UserProfile):
        relative_file_path = "save_game_" + user.get_user_name() + ".p"
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, "saves", relative_file_path)
        ret: Game = None
        try:
            ret = pickle.load(open(file_path, "rb"))
            return ret
        except:
            print("Failed to load game")
            return ret

    def get_player_board_canvas(self):
        return self.player1.fleet_board.canvas

    def get_player_ship_placement_canvas(self):
        return PlaceShipsMenuCanvas(self.player1.fleet_board.canvas)

    def get_take_turn_canvas(self):
        return TakeTurnCanvas(self.player1.fleet_board.canvas, self.player1.target_board.canvas)

    def position_player_fleet(self, player: Player):
        for ship_type in player.ships_to_place:
            if not player.is_ai:
                self.view.update_display(PlaceShipsCanvas(player.fleet_board.canvas, ship_type))
            ship = player.position_ship(ship_type)
            if not player.is_ai:
                player.fleet_board.canvas.update_ship_cells(ship.tiles)
        if not player.is_ai:
            self.view.update_display(FinishedPlacingShipsCanvas(player.fleet_board.canvas))

    def position_fleets(self, dry_run=False):

        self.position_player_fleet(self.player2)
        self.position_player_fleet(self.player1)

