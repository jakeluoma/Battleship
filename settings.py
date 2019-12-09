import canvas
# have to do "import canvas" due to circular import with canvas
from enum import Enum
from view import InputParser

class SettingsOption(Enum):
    CHANGE_SHIP_CELL = 0
    CHANGE_HIT_CELL = 1
    CHANGE_MISS_CELL = 2
    NEW_GAME = 3


class Settings:

    empty_cell = '_'
    ship_cell = '1'
    hit_cell = 'X'
    missed_cell = 'O'


    @staticmethod
    def configure_settings():
        # canvas.configure_display_start_canvas.paint()
        settings_inp = input()
        option = InputParser.parse_settings(settings_inp)
        if option == 0:
            Settings.change_ship_cell()
        elif option == 1:
            Settings.change_hit_cell()
        elif option == 2:
            Settings.change_missed_cell()
        return

    @staticmethod
    def change_empty_cell():
        canvas.empty_cell_change_request_canvas.paint()
        canvas.character_entry_request_canvas.paint()
        Settings.empty_cell = input()
        canvas.empty_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_ship_cell():
        canvas.character_entry_request_canvas.paint()
        Settings.ship_cell = input()
        while(True):
            if Settings.ship_cell == Settings.empty_cell:
                canvas.enter_again_request_canvas.paint()
                Settings.ship_cell = input()
                continue
            else:
                break
        canvas.not_hit_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_hit_cell():
        canvas.character_entry_request_canvas.paint()
        Settings.hit_cell = input()
        while (True):
            if Settings.hit_cell == Settings.empty_cell or Settings.hit_cell == Settings.ship_cell:
                canvas.enter_again_request_canvas.paint()
                Settings.hit_cell = input()
                continue
            else:
                break
        canvas.hit_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_missed_cell():
        canvas.character_entry_request_canvas.paint()
        Settings.missed_cell = input()
        while (True):
            if Settings.missed_cell in [Settings.empty_cell, Settings.ship_cell, Settings.hit_cell]:
                canvas.enter_again_request_canvas.paint()
                Settings.missed_cell = input()
                continue
            else:
                break
        canvas.miss_cell_changed_canvas.paint()
        return