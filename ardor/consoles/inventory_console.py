import tcod
import tabulate

from .console import Console

from ardor.inventory import Inventory
from ardor.util import clamp


MENU_SIZE = 5


class InventoryConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Inventory) -> None:
        super().__init__(x, y, width, height)
        self.target = target
        self.headings = [
            " ",
            "Name".ljust(10),
            "Mass",
            "Size"
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

    def inventory_index(self) -> int:
        return self.cursor + (self.page * MENU_SIZE)

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, p) -> None:
        max_page = (len(self.target.contents) // MENU_SIZE)
        self._page = clamp(p, 0, max_page)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.dark_grey

        self.console.print_frame(
            1, 1, self.width - 2, self.height - 2, clear=False
        )

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
            self.headings, tablefmt="simple", floatfmt=".2f"
        ).split("\n")

        headings = lines[0:2]
        lines = lines[2:]

        back_msg = "ESC: back"
        self.console.print_(
            self.width - 3 - len(back_msg), self.height - 2,
            back_msg, tcod.BKGND_SET, tcod.LEFT
        )

        offset_x = (self.width - len(headings[0])) // 2
        offset_y = 3

        for i, l in enumerate(headings):
            self.console.print_(
                offset_x, i + offset_y, l, tcod.BKGND_SET, tcod.LEFT
            )

        cap_string = "Size Used: {:.2f}/{:.2f}".format(
            self.target.max_capacity - self.target.capacity,
            self.target.max_capacity
        )

        self.console.print_(
            self.width - 2 - len(cap_string), self.height - 4,
            cap_string, tcod.BKGND_SET, tcod.LEFT
        )

        if len(lines) == 0:
            return

        for i in range(len(lines)):
            self.console.print_(
                offset_x, i + len(headings) + offset_y,
                lines[i], tcod.BKGND_SET, tcod.LEFT
            )

        item = self.target.contents[self.inventory_index()]

        actions = " | ".join(
            ["{}: {}".format(sym, name) for name, sym in item.actions]
        )

        self.console.print_(
            3, self.height - 2,
            actions, tcod.BKGND_SET, tcod.LEFT
        )

    def _draw_cursor(self, pos: int) -> str:
        return "x" if self.cursor == pos else " "
