import tcod

from ardor.entity import Battler
from ardor.stats import Stats
from ardor.inventory import Inventory


class Player(Battler):

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str, stats: Stats) -> None:
        super().__init__(initial_x, initial_y, symbol, stats)

        self.inventory = Inventory(20.0)

        self.color = tcod.white

        self.torch = False
        self.lit = True
