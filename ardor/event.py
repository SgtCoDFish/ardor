import abc


class GameEvent(abc.ABC):

    def __init__(self, msg: str, emit: bool=False):
        self.msg = msg
        self.emit = emit

    @abc.abstractmethod
    def process(self):
        pass

    def __str__(self) -> str:
        return self.msg
