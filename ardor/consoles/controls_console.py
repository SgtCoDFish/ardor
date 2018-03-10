import tcod

from .console import Console

CONTROLS_TEXT = """
     Move / Attack:


     %ck%c          %cup%c
   %ch%c   %cl%c   %cleft%c    %cright%c
     %cj%c         %cdown%c


%ci%c: inventory | %c,%c: pick up
%c<%c: descend   | %cb%c: blast
""" % (
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP,
    tcod.COLCTRL_3, tcod.COLCTRL_STOP
)


class ControlsConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def render(self) -> None:
        self.clear()
        self.console.default_fg = tcod.white
        self.console.default_bg = tcod.black
        tcod.console_set_color_control(tcod.COLCTRL_1, tcod.red, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_2, tcod.yellow, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_3, tcod.green, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_4, tcod.white, tcod.black)

        self.console.print_frame(
            1, 1, self.width - 2, self.height - 2, clear=False
        )

        self.console.print_(
            3, 3, CONTROLS_TEXT
        )
