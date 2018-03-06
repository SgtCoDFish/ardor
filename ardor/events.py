import abc

from ardor.entity import Entity
from ardor.item import Item


class GameEvent(abc.ABC):

    def __init__(self, msg: str, emit: bool=False) -> None:
        self.msg = msg
        self.emit = emit

    def process(self) -> None:
        pass

    def __str__(self) -> str:
        return self.msg


class MovementEvent(GameEvent):

    def __init__(self, entity: Entity, new_x, new_y) -> None:
        super().__init__("{} moved to ({}, {})".format(
            entity.symbol, new_x, new_y
        ), emit=False)
        self.entity = entity

        self.new_x = new_x
        self.new_y = new_y

    def process(self) -> None:
        pass


class PickupEvent(GameEvent):

    def __init__(self, entity: Entity, item: Item) -> None:
        super().__init__("{} picked up {}".format(
            entity.symbol, item.name
        ), emit=True)

        self.entity = entity
        self.item = item


class ItemDroppedEvent(GameEvent):

    def __init__(self, entity: Entity, item: Item) -> None:
        super().__init__("{} dropped {}".format(
            entity.symbol, item.name
        ), emit=True)

        self.entity = entity
        self.item = item


class InventoryFullEvent(GameEvent):

    def __init__(self, entity: Entity, item: Item) -> None:
        super().__init__("{} failed to pick up {}".format(
            entity.symbol, item.name
        ), emit=True)

        self.entity = entity
        self.item = item


class NothingThereEvent(GameEvent):

    def __init__(self) -> None:
        super().__init__("There's nothing there!", emit=True)


class HealingPotionEvent(GameEvent):

    def __init__(self, entity: Entity, potency: int) -> None:
        super().__init__("{} healed for {} with the potion".format(
            entity.symbol, potency
        ), emit=True)
        self.entity = entity
        self.potency = potency
