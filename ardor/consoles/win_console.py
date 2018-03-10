import tcod

from .console import Console

WIN_TEXT = """
            Congratulations, you won!

Feel free to e-mail me for place in a hall-of-fame
               on my website!

        ashley_davis10419@hotmail.com

 (There's nothing left to do but close the game)"""


class WinConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.dark_grey

        self.console.print_frame(
            1, 1, self.width - 2, self.height - 2, clear=False
        )

        self.console.print_(
            3, 3, WIN_TEXT
        )
