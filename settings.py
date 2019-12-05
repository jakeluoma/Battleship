class Settings:

    empty_cell = '_'
    ship_cell = '1'
    hit_cell = 'X'
    missed_cell = 'O'

    @staticmethod
    def configure_settings():
        Settings.change_empty_cell()
        Settings.change_ship_cell()
        Settings.change_hit_cell()
        Settings.change_missed_cell()
        return

    @staticmethod
    def change_empty_cell():
        yes_no = input("1. Do you want to change the representation of empty cell ? (Y|N): ")
        if yes_no == 'Y' or yes_no == 'y' or yes_no == 'YES' or yes_no == 'Yes' or yes_no == 'yes':
            Settings.empty_cell = input(" - Please enter character of your choice: ")
            print("===Empty cell representation updated successfully===")
        return

    @staticmethod
    def change_ship_cell():
        yes_no = input("2. Do you want to change the representation of ship cell (not hit) ? (Y|N): ")

        if yes_no == 'Y' or yes_no == 'y' or yes_no == 'YES' or yes_no == 'Yes' or yes_no == 'yes':
            Settings.ship_cell = input(" - Please enter character of your choice: ")
            while(True):
                if Settings.ship_cell == Settings.empty_cell:
                    Settings.ship_cell = input(" - Please enter again: ")
                    continue
                else:
                    break

            print("===Ship cell (not hit) representation updated successfully===")
        return

    @staticmethod
    def change_hit_cell():
        yes_no = input("3. Do you want to change the representation of hit cell ? (Y|N): ")

        if yes_no == 'Y' or yes_no == 'y' or yes_no == 'YES' or yes_no == 'Yes' or yes_no == 'yes':
            Settings.empty_cell = input(" - Please enter character of your choice: ")
            while (True):
                if Settings.hit_cell == Settings.empty_cell or Settings.hit_cell == Settings.ship_cell:
                    Settings.hit_cell = input(" - Please enter again: ")
                    continue
                else:
                    break

            print("===Hit cell representation updated successfully===")
        return

    @staticmethod
    def change_missed_cell():
        yes_no = input("4. Do you want to change the representation of missed cell ? (Y|N): ")

        if yes_no == 'Y' or yes_no == 'y' or yes_no == 'YES' or yes_no == 'Yes' or yes_no == 'yes':
            Settings.missed_cell = input(" - Please enter character of your choice: ")
            while (True):
                if Settings.missed_cell == Settings.empty_cell or Settings.missed_cell == Settings.ship_cell \
                        or Settings.missed_cell == Settings.hit_cell:
                    Settings.ship_cell = input(" - Please enter again: ")
                    continue
                else:
                    break


            print("===Missed cell representation updated successfully===")
        return