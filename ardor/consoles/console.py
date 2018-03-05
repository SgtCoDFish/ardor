import abc
import tcod


class Console(abc.ABC):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.console = tcod.console_new(self.width, self.height)

    @abc.abstractmethod
    def render(self) -> None:
        pass

    def blit(self, target: tcod.console.Console) -> None:
        self.console.blit(
            0, 0, self.width, self.height,
            target, self.x, self.y)

    def clear(self) -> None:
        tcod.console_clear(self.console)
