from enum import Enum


class State(Enum):
    PLAY = 1
    INVENTORY = 2
    EQUIP_SPELL = 3
    AIMING = 4
    WON = 5
    INTRO = 6
    GAME_OVER = 7
