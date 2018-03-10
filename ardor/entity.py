import tcod
import math

from ardor.stats import Stats
from ardor.colors import LIGHT_GROUND


class Entity:

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str) -> None:
        self.x = initial_x
        self.y = initial_y

        self.symbol = symbol[0]

        self.lit = False

        self.walkable = False
        self.color = tcod.grey

    def move_to(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

    def draw(self, console: tcod.console.Console) -> None:
        tcod.console_put_char_ex(console, self.x, self.y,
                                 self.symbol, self.color, LIGHT_GROUND)

    def distance_to(self, other: 'Entity') -> float:
        xdiff = self.x - other.x
        ydiff = self.y - other.y

        return math.sqrt(xdiff * xdiff + ydiff * ydiff)


class Battler(Entity):

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str, stats: Stats) -> None:
        super().__init__(initial_x, initial_y, symbol)
        self.stats = stats


class Stairs(Entity):

    def __init__(self, initial_x: int, initial_y: int) -> None:
        super().__init__(initial_x, initial_y, '<')
        self.walkable = True
