import tcod

from .console import Console

from collections import deque
from ardor.events import GameEvent

from typing import List


class EventConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.event_messages = deque(maxlen=(self.height - 1))  # type: deque

    def add_events(self, events: List[GameEvent]) -> None:
        for e in events:
            if e.emit:
                self.event_messages.appendleft(str(e))

    def render(self) -> None:
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black

        for i, ev in enumerate(self.event_messages):
            self.console.print_(
                0, self.height - i - 1,
                ev.ljust(self.width),
                tcod.BKGND_SET, tcod.LEFT
            )
