# have to do "import canvas" due to circular import with canvas
from canvas import empty_cell_change_request_canvas, character_entry_request_canvas, empty_cell_changed_canvas, \
    not_hit_cell_changed_canvas, enter_again_request_canvas, miss_cell_changed_canvas, hit_cell_changed_canvas
from options import CellConfig
from view import InputParser


class Settings:
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
        empty_cell_change_request_canvas.paint()
        character_entry_request_canvas.paint()
        CellConfig.empty_cell = input()
        empty_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_ship_cell():
        character_entry_request_canvas.paint()
        CellConfig.ship_cell = input()
        while(True):
            if CellConfig.ship_cell == CellConfig.empty_cell:
                enter_again_request_canvas.paint()
                CellConfig.ship_cell = input()
                continue
            else:
                break
        not_hit_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_hit_cell():
        character_entry_request_canvas.paint()
        CellConfig.hit_cell = input()
        while (True):
            if CellConfig.hit_cell == CellConfig.empty_cell or CellConfig.hit_cell == CellConfig.ship_cell:
                enter_again_request_canvas.paint()
                CellConfig.hit_cell = input()
                continue
            else:
                break
        hit_cell_changed_canvas.paint()
        return

    @staticmethod
    def change_missed_cell():
        character_entry_request_canvas.paint()
        CellConfig.missed_cell = input()
        while (True):
            if CellConfig.missed_cell in [CellConfig.empty_cell, CellConfig.ship_cell, CellConfig.hit_cell]:
                enter_again_request_canvas.paint()
                CellConfig.missed_cell = input()
                continue
            else:
                break
        miss_cell_changed_canvas.paint()
        return