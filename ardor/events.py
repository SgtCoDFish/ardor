import abc

from ardor.entity import Entity
from ardor.attack import Attack
from ardor.item import Item, HealingPotion


class GameEvent(abc.ABC):

    def __init__(self, msg: str, emit: bool=False, steps: int=0) -> None:
        self.msg = msg
        self.emit = emit
        self.steps = steps

    def process(self) -> None:
        pass

    def __str__(self) -> str:
        return self.msg


class MovementEvent(GameEvent):

    def __init__(self, entity: Entity, new_x, new_y) -> None:
        super().__init__("{} moved to ({}, {})".format(
            entity.symbol, new_x, new_y
        ), emit=False, steps=1)
        self.entity = entity

        self.new_x = new_x
        self.new_y = new_y


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

    def __init__(self, entity: Entity, potion: HealingPotion) -> None:
        super().__init__("{} healed for {} with the {}".format(
            entity.symbol, potion.potency, potion.name
        ), emit=True)
        self.entity = entity
        self.potion = potion


class CapifyEvent(GameEvent):

    def __init__(self, entity: Entity, target: Item, caps: float) -> None:
        super().__init__("{} capified {} for {:.2f} caps".format(
            entity.symbol, target.name, caps
        ), emit=True)


class AttackEvent(GameEvent):

    def __init__(self, attack: Attack) -> None:
        super().__init__("{} attacked {} for {}".format(
            attack.attacker.symbol, attack.target.symbol, attack.damage
        ), emit=True, steps=1)
        self.attack = attack


class DeathEvent(GameEvent):

    def __init__(self, entity: Entity, reason: Attack) -> None:
        super().__init__("{} died from a {} attack".format(
            entity.symbol, reason.pretty
        ), emit=True)
        self.entity = entity
        self.reason = reason


class PlayerDeathEvent(GameEvent):

    def __init__(self, entity: Entity, reason: Attack) -> None:
        super().__init__("{} died from a {} attack".format(
            entity.symbol, reason.pretty
        ), emit=True)
        self.entity = entity
        self.reason = reason
