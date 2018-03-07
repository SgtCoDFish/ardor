import tcod
import math

from ardor.stats import Stats


class Entity:

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str) -> None:
        self.x = initial_x
        self.y = initial_y

        self.symbol = symbol[0]

        self.lit = False

        self.walkable = False

    def move_to(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

    def draw(self, console: tcod.console.Console) -> None:
        tcod.console_put_char(console, self.x, self.y,
                              self.symbol, tcod.BKGND_NONE)

    def distance_to(self, other: 'Entity') -> float:
        xdiff = self.x - other.x
        ydiff = self.y - other.y

        return math.sqrt(xdiff * xdiff + ydiff * ydiff)

    def undraw(self, console: tcod.console.Console) -> None:
        tcod.console_put_char(console, self.x, self.y,
                              " ", tcod.BKGND_NONE)


class Battler:

    def __init__(self, stats: Stats) -> None:
        self.stats = stats
