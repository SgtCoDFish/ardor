import tcod
import tabulate

from .console import Console

from ardor.inventory import Inventory


MENU_SIZE = 5


def clamp(n: int, smallest: int, largest: int) -> None:
    return max(smallest, min(n, largest))


class InventoryConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Inventory) -> None:
        super().__init__(x, y, width, height)
        self.target = target
        self.headings = [
            " ",
            "Name".ljust(13),
            "Mass",
            "Volume"
        ]
        self._cursor = 0
        self._page = 0

    @property
    def cursor(self) -> int:
        return self._cursor

    @cursor.setter
    def cursor(self, val) -> None:
        if val < 0:
            if self.page > 0:
                self.page -= 1
                self._cursor = MENU_SIZE - 1
                return
        elif val >= MENU_SIZE:
            if self.page < (len(self.target.contents) // MENU_SIZE):
                self.page += 1
                self._cursor = 0
                return

        if self.page == (len(self.target.contents) // MENU_SIZE):
            maxval = (len(self.target.contents) % MENU_SIZE)
        else:
            maxval = MENU_SIZE

        self._cursor = clamp(val, 0, maxval - 1)

    @property
    def page(self) -> int:
        return self._page

    def inventory_index(self) -> int:
        return self.cursor + (self.page * MENU_SIZE)

    @page.setter
    def page(self, p) -> None:
        max_page = (len(self.target.contents) // MENU_SIZE)
        self._page = clamp(p, 0, max_page)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.red

        inv_count = len(self.target.contents)

        if inv_count == 0:
            self.cursor = -1
        elif self.cursor >= inv_count:
            self.cursor = 0

        lines = tabulate.tabulate(
            [[self._draw_cursor(i), v.name, v.mass, v.volume] for i, v in
             enumerate(
                 self.target.contents[
                     self._page * MENU_SIZE:(self._page + 1) * MENU_SIZE
                 ])],
            self.headings, tablefmt="simple"
        ).split("\n")

        headings = lines[0:2]
        lines = lines[2:]

        offset_x = (self.width - len(lines[0])) // 2

        for i, l in enumerate(headings):
            self.console.print_(
                offset_x, i + 1, l, tcod.BKGND_SET, tcod.LEFT
            )

        for i in range(len(lines)):
            self.console.print_(
                offset_x, i + len(headings) + 1,
                lines[i], tcod.BKGND_SET, tcod.LEFT
            )

        self.console.print_(
            1, self.height - 2,
            "Space: Print", tcod.BKGND_SET, tcod.LEFT
        )

    def _draw_cursor(self, pos: int) -> str:
        return "x" if self.cursor == pos else " "
