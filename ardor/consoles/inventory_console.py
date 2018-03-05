import tcod
import tabulate

from .console import Console

from ardor.inventory import Inventory


class InventoryConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Inventory) -> None:
        super().__init__(x, y, width, height)
        self.target = target
        self.headings = [
            "Name",
            "Mass",
            "Volume"
        ]

    def render(self) -> None:
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.black

        lines = tabulate.tabulate(
            [[i.name, i.mass, i.volume] for i in self.target.contents],
            self.headings, tablefmt="grid"
        ).split("\n")

        for i, v in enumerate(lines):
            self.console.print_(
                1, i + 1, v, tcod.BKGND_SET, tcod.LEFT
            )
