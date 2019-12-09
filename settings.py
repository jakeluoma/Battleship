import canvas
# have to do "import canvas" due to circular import with canvas

class Settings:

    empty_cell = '_'
    ship_cell = '1'
    hit_cell = 'X'
    missed_cell = 'O'

    @staticmethod
    def configure_settings():
        canvas.configure_display_start_canvas.display_string()
        # Settings.change_empty_cell()
        Settings.change_ship_cell()
        Settings.change_hit_cell()
        Settings.change_missed_cell()
        return

    @staticmethod
    def change_empty_cell():
        canvas.empty_cell_change_request_canvas.display_string()
        yes_no = input()
        if yes_no in ['Y', 'y', 'YES', 'Yes', 'yes']:
            canvas.character_entry_request_canvas.display_string()
            Settings.empty_cell = input()
            canvas.empty_cell_changed_canvas.display_string()
        return

    @staticmethod
    def change_ship_cell():
        canvas.not_hit_cell_change_request_canvas.display_string()
        yes_no = input()

        if yes_no in ['Y', 'y', 'YES', 'Yes', 'yes']:
            canvas.character_entry_request_canvas.display_string()
            Settings.ship_cell = input()
            while(True):
                if Settings.ship_cell == Settings.empty_cell:
                    canvas.enter_again_request_canvas.display_string()
                    Settings.ship_cell = input()
                    continue
                else:
                    break
            canvas.not_hit_cell_changed_canvas.display_string()
        return

    @staticmethod
    def change_hit_cell():
        canvas.hit_cell_change_request_canvas.display_string()
        yes_no = input()

        if yes_no in ['Y', 'y', 'YES', 'Yes', 'yes']:
            canvas.character_entry_request_canvas.display_string()
            Settings.empty_cell = input()
            while (True):
                if Settings.hit_cell == Settings.empty_cell or Settings.hit_cell == Settings.ship_cell:
                    canvas.enter_again_request_canvas.display_string()
                    Settings.ship_cell = input()
                    continue
                else:
                    break
            canvas.hit_cell_changed_canvas.display_string()
        return

    @staticmethod
    def change_missed_cell():
        canvas.miss_cell_change_request_canvas.display_string()
        yes_no = input()

        if yes_no in ['Y', 'y', 'YES', 'Yes', 'yes']:
            canvas.character_entry_request_canvas.display_string()
            Settings.empty_cell = input()
            while (True):
                if Settings.missed_cell in [Settings.empty_cell, Settings.ship_cell, Settings.hit_cell]:
                    canvas.enter_again_request_canvas.display_string()
                    Settings.ship_cell = input()
                    continue
                else:
                    break
            canvas.miss_cell_changed_canvas.display_string()
        return