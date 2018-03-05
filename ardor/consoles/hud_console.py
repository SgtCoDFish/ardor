import tcod

from .console import Console

from ardor.entity import Entity


class HUDConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Entity) -> None:
        super().__init__(x, y, width, height)
        self.target = target

    def render(self) -> None:
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black

        self.console.print_(
            0, 0, "{} HP: {}/{}".format(
                self.target.symbol,
                self.target.stats.hp,
                self.target.stats.max_hp
            ).ljust(self.width), tcod.BKGND_SET, tcod.LEFT
        )
