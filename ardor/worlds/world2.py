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

    items = [ItemEntity(
        6, 2, Fuel('u', "Uranium", 0.75, 2, 40.0)
    ), ItemEntity(
        12, 12, Fuel('w', "Hardwood", random.random() * 5, 3, 3.0)
    )]

    mobs = [
        Mob(2, 2, 'D', Stats(9, 7, 6, 1, 1, 2), AIType.MINDLESS,
            [HealingPotion(4),
             Fuel('o', "Oil", 2.00, 2, 15.0),
             Item('b', "Bone", 2.0, 1)]),
        Mob(32, 10, 'D', Stats(9, 7, 6, 1, 1, 2), AIType.MINDLESS,
            [HealingPotion(4),
             Fuel('o', "Oil", 2.00, 2, 15.0),
             Fuel('o', "Oil", 2.25, 2, 15.0),
             Fuel('o', "Oil", 2.50, 2, 15.0),
             Fuel('o', "Oil", 2.75, 2, 15.0)]),
        Mob(34, 10, 'd', Stats(9, 7, 6, 1, 1, 2), AIType.MINDLESS,
            [HealingPotion(4), HealingPotion(8),
             Fuel('o', "Oil", 1.50, 2, 15.0),
             Item('b', "Bone", 2.0, 1)])
    ]
