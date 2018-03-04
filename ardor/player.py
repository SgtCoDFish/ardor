from ardor.entity import Entity, Battler
from ardor.stats import Stats
from ardor.inventory import Inventory


class Player(Entity, Battler):

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str, stats: Stats) -> None:
        Entity.__init__(self, initial_x, initial_y, symbol)
        Battler.__init__(self, stats)

        self.inventory = Inventory(20.0)

        self.torch = True
        self.lit = True
