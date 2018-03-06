import tcod

from .console import Console

from ardor.player import Player


class HUDConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Player) -> None:
        super().__init__(x, y, width, height)
        self.target = target

    def render(self) -> None:
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black

        self.console.print_(
            0, 0, "{} HP: {}/{}\n CAP: {:.2f}/{:.2f}".format(
                self.target.symbol,
                self.target.stats.hp,
                self.target.stats.max_hp,
                self.target.stats.cap,
                self.target.stats.max_cap
            ).ljust(self.width), tcod.BKGND_SET, tcod.LEFT
        )
