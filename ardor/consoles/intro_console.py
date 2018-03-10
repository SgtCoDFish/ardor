import tcod

from .console import Console

INTRO_TEXT = """
           Welcome to %cARDOR%c!
           -----------------

 Try to reach the bottom of the dungeon!

 Remember that all items can be "capped"
         to create energy for
      your attacks and your torch!



         Press %cSPACE%c to start!
""" % (
    tcod.COLCTRL_2, tcod.COLCTRL_STOP,
    tcod.COLCTRL_1, tcod.COLCTRL_STOP
)


class IntroConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.dark_grey
        tcod.console_set_color_control(tcod.COLCTRL_1, tcod.green, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_2, tcod.yellow, tcod.black)

        self.console.print_frame(
            1, 1, self.width - 2, self.height - 2, clear=False
        )

        self.console.print_(
            3, 3, INTRO_TEXT
        )
