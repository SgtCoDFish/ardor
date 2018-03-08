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
        self.clear()
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black
        tcod.console_set_color_control(tcod.COLCTRL_1, tcod.red, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_2, tcod.yellow, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_3, tcod.green, tcod.black)
        tcod.console_set_color_control(tcod.COLCTRL_4, tcod.white, tcod.black)

        hp_percentage = (self.target.stats.hp / self.target.stats.max_hp) * 100

        if hp_percentage >= 75.0:
            hp_color = tcod.COLCTRL_3
        elif hp_percentage >= 25.0:
            hp_color = tcod.COLCTRL_2
        else:
            hp_color = tcod.COLCTRL_1

        torch_status = self.target.torch

        if torch_status:
            torch_color = tcod.COLCTRL_2
        else:
            torch_color = tcod.COLCTRL_4

        hud_lines = "\n".join([
            "%c{}%c the %cBarbarian%c" % (
                tcod.COLCTRL_4, tcod.COLCTRL_STOP,
                tcod.COLCTRL_4, tcod.COLCTRL_STOP
            ),
            "",
            "HP: %c{}%c/%c{}%c" % (
                hp_color, tcod.COLCTRL_STOP,
                tcod.COLCTRL_4, tcod.COLCTRL_STOP
            ),
            "CAP: %c{:.2f}%c/%c{:.2f}%c" % (
                tcod.COLCTRL_4, tcod.COLCTRL_STOP,
                tcod.COLCTRL_4, tcod.COLCTRL_STOP
            ),
            "TORCH: %c{}%c" % (torch_color, tcod.COLCTRL_STOP)
        ])

        self.console.print_(
            0, 0, hud_lines.format(
                self.target.symbol,
                self.target.stats.hp,
                self.target.stats.max_hp,
                self.target.stats.cap,
                self.target.stats.max_cap,
                "ON" if self.target.torch else "OFF"
            ).ljust(self.width), tcod.BKGND_SET, tcod.LEFT
        )
