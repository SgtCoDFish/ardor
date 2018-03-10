from ardor.item import Item, ItemEntity, Fuel, HealingPotion
from ardor.mobs import Mob
from ardor.stats import Stats
from ardor.ai import AIType

from . import World


WORLD3_MAP = [
    '######################################',
    '#       ######################       #',
    '#       ######################       #',
    '#                ===                 #',
    '#       ######## ### #########       #',
    '#       ########     #########       #',
    '################## ###################',
    '################## ###################',
    '################## ###################',
    '################## ###################',
    '################## ###################',
    '################## ###################',
    '############             #############',
    '############                 #########',
    '############             ### #########',
    '############        ###=#### #########',
    '############        #    ### #########',
    '############        =  <     #########',
    '############        #    #############',
    '######################################',
]


class World3(World):

    base_map = WORLD3_MAP
    width = 38
    height = 20
    y = 1

    player_start_x = 3
    player_start_y = 3

    items = [ItemEntity(
        6, 2, HealingPotion(10)
    ), ItemEntity(
        34, 3, Fuel(
            "c", "Coal", 15.0, 8, 2.0
        )
    ), ItemEntity(
        34, 4, Fuel(
            "A", "Breastplate", 15.0, 7, 2.5
        )
    ), ItemEntity(
        13, 17, HealingPotion(6)
    )]

    mobs = [
        Mob(13, 17, 'Q', Stats(12, 10, 6, 1, 1, 2), AIType.MINDLESS,
            [Item('q', "Queen's Amulet", 2.0, 1)])
    ]
