from enum import Enum


class SettingsOption(Enum):
    CHANGE_SHIP_CELL = 0
    CHANGE_HIT_CELL = 1
    CHANGE_MISS_CELL = 2
    NEW_GAME = 3


class MenuOption(Enum):
    STARTMENU = 0
    LOGIN = 1
    EXIT = 2
    MAINMENU = 3
    NEWGAMEMENU = 4
    SHOWSTATS = 5
    PLACESHIPSMENU = 6
    VIEWCONFIG = 7
    PLACESHIPS = 8
    FINISHEDPLACING = 9
    STARTGAME = 10
    GAMEOVER = 11
    LOGOUT = 12
    LOADGAME = 13
    SHIPCELL = 14
    HITCELL = 15
    MISSCELL = 16


class CellConfig:
    empty_cell = '_'
    ship_cell = '1'
    hit_cell = 'X'
    missed_cell = 'O'
