import tcod

from .console import Console

GAME_OVER_TEXT = """
           %cGAME OVER!%c
           ----------

Please try again by restarting
              %cARDOR%c!

       Thanks for playing!
""" % (
    tcod.COLCTRL_1, tcod.COLCTRL_STOP,
    tcod.COLCTRL_1, tcod.COLCTRL_STOP
)


class GameOverConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.black
        self.console.default_bg = tcod.white
        tcod.console_set_color_control(tcod.COLCTRL_1, tcod.red, tcod.black)
        self.console.print_frame(
            1, 1, self.width - 2, self.height - 2, clear=False
        )

        self.console.print_(
            3, 3, GAME_OVER_TEXT
        )
