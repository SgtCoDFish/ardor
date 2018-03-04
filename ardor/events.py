import abc

from ardor.entity import Entity


class GameEvent(abc.ABC):

    def __init__(self, msg: str, emit: bool=False) -> None:
        self.msg = msg
        self.emit = emit

    @abc.abstractmethod
    def process(self) -> None:
        pass

    def __str__(self) -> str:
        return self.msg


class MovementEvent(GameEvent):

    def __init__(self, entity: Entity, new_x, new_y) -> None:
        super().__init__("{} moved to ({}, {})".format(
            entity.symbol, new_x, new_y
        ), emit=True)
        self.entity = entity

        self.new_x = new_x
        self.new_y = new_y

    def process(self) -> None:
        pass
