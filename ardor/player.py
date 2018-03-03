from ardor.entity import Entity, Battler
from ardor.stats import Stats


class Player(Entity, Battler):

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str, stats: Stats) -> None:
        Entity.__init__(self, initial_x, initial_y, symbol)
        Battler.__init__(self, stats)
