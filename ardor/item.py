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
        self.energy_density = 0.5
        self.actions = [("drop", "d"), ("capify", "c")] + actions


class Fuel(Item):

    def __init__(self, symbol: str, name: str, mass: float, volume: int,
                 energy_density: float) -> None:
        super().__init__(symbol, name, mass, volume)
        self.energy_density = energy_density


class HealingPotion(Item):

    def __init__(self, potency: int) -> None:
        super().__init__('P', "Healing Potion",
                         1.0, 2, [("quaff", "q")])
        self.potency = potency


class ItemEntity(Entity):

    def __init__(self, x: int, y: int, item: Item) -> None:
        Entity.__init__(self, x, y, item.symbol)
        self.item = item
        self.walkable = True
