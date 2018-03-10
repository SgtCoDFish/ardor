import random

from ardor.item import Item, ItemEntity, Fuel, HealingPotion
from ardor.mobs import Mob
from ardor.stats import Stats
from ardor.ai import AIType

from . import World


WORLD1_MAP = [
    '##############################################',
    '#######################      #################',
    '######    ###########    #     ###############',
    '#####      ###########  ###        #         #',
    '####        ######      #####      =         #',
    '###         ####       ########    #         #',
    '###         ###      ###########  ######## ###',
    '######### ######    ######             ### ###',
    '########   #######  ######   #     #   ### ###',
    '########   ######      ###                 ###',
    '########                               #######',
    '####       ######      ###   #     #   #######',
    '#### ###   ########## ####             #######',
    '#### ###   ##########   ###########=##########',
    '#### ##################   #####          #####',
    '#### ###             #### #####    <     #####',
    '####           #     ####                #####',
    '########       #     #### #####          #####',
    '########       #####      ####################',
    '##############################################',
]


class World1(World):

    base_map = WORLD1_MAP
    width = 46
    height = 20
    y = 1

    player_start_x = 20
    player_start_y = 10

    items = [ItemEntity(
        40, 14, Item("d", "Dagger", 1.0, 3)
    ), ItemEntity(
        6, 5, Item("s", "Sword", 2.0, 6)
    ), ItemEntity(
        21, 2, Fuel(
            "w", "Oak Wood", 3.0 + random.random(), 2, 2.5
        )
    ), ItemEntity(
        37, 4, HealingPotion(7)
    )]

    mobs = [
        Mob(25, 10, 'G', Stats(5, 5, 6, 1, 1, 2), AIType.MINDLESS,
            [Item('/', "Stick", 1.50, 1),
             Item('\\', "Stick", 1.75, 1),
             Item('/', "Stick", 1.50, 1),
             Item('b', "Bone", 2.0, 1)]),
        Mob(11, 17, 'G', Stats(5, 5, 6, 1, 1, 2), AIType.MINDLESS,
            [Item('/', "Stick", 1.50, 1),
             Item('\\', "Stick", 1.75, 1),
             HealingPotion(4),
             Item('/', "Stick", 1.50, 1),
             Item('b', "Bone", 2.0, 1)]),
        Mob(32, 4, 'w', Stats(10, 25, 5, 2, 6, 4), AIType.MINDLESS,
            [Item('/', "Stick", 1.5, 1),
             HealingPotion(6),
             Fuel('u', "Uranium", 0.75, 2, 40.0)])
    ]
