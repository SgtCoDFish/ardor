from ardor.entity import Entity


class Item:

    def __init__(self, name: str, mass: float, volume: int) -> None:
        self.name = name
        self.mass = mass
        self.volume = volume
        self.density = self.mass / self.volume


class ItemEntity(Entity):

    def __init__(self, x: int, y: int, symbol: str, item: Item) -> None:
        Entity.__init__(self, x, y, symbol)
        self.item = item
