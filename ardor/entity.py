import tcod

from ardor.stats import Stats


class Entity:

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str) -> None:
        self.x = initial_x
        self.y = initial_y

        self.symbol = symbol[0]

    def move_to(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def draw(self, console: tcod.console.Console):
        tcod.console_put_char(console, self.x, self.y,
                              self.symbol, tcod.BKGND_NONE)


class Battler:

    def __init__(self, stats: Stats) -> None:
        self.stats = stats
