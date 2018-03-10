import random

from ardor.item import Item, ItemEntity, Fuel, HealingPotion
from ardor.mobs import Mob
from ardor.stats import Stats
from ardor.ai import AIType

from . import World


WORLD2_MAP = [
    '##########################################',
    '#      ##      ###########              ##',
    '#      ==           ######              ##',
    '#      ##      #### ######              ##',
    '#      ##      #### ######              ##',
    '### ###############                     ##',
    '### ############### ######              ##',
    '### ############### ######              ##',
    '### ############### ######              ##',
    '###                 ############=#########',
    '### ########=##################    #######',
    '### #####       ###############    #######',
    '### #####       #############      #######',
    '### #####       ############# # <  #######',
    '### ######## ################ #    #######',
    '###                           =    #######',
    '##########################################',
]


class World2(World):

    base_map = WORLD2_MAP
    width = 42
    height = 17
    y = 1

    player_start_x = 37
    player_start_y = 4

    items = []

    mobs = []
