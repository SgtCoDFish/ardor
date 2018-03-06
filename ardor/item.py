from ardor.entity import Entity

from typing import List, Tuple


class Item:

    def __init__(self, symbol: str, name: str,
                 mass: float, volume: int,
                 actions: List[Tuple[str, str]]=None) -> None:
        if actions is None:
            actions = []

        self.symbol = symbol
        self.name = name
        self.mass = mass
        self.volume = volume
        self.actions = [("drop", "d")] + actions


class ItemEntity(Entity):

    def __init__(self, x: int, y: int, item: Item) -> None:
        Entity.__init__(self, x, y, item.symbol)
        self.item = item
