from enum import Enum
from ardor.item import Item
from typing import List  # noqa


class PickupResult(Enum):
    SUCCESS = 0
    TOO_BIG = 1
    TOO_HEAVY = 2


class Inventory:

    def __init__(self, max_capacity: float) -> None:
        self.contents = []  # type: List[Item]

        self.max_capacity = max_capacity
        self.capacity = self.max_capacity

    def add_item(self, item: Item) -> PickupResult:
        # print("We have", self.capacity, "; trying to pick up", item.volume)
        if item.volume > self.capacity:
            return PickupResult.TOO_BIG

        self.contents.append(item)
        self.capacity -= item.volume

        return PickupResult.SUCCESS

    def remove_item(self, item: Item) -> bool:
        try:
            self.contents.remove(item)
        except ValueError:
            print("WARNING: Tried to remove", item.name, "but not found")
            return False

        self.capacity += item.volume
        return True

    def size(self) -> int:
        return len(self.contents)
