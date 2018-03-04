import tcod

from collections import deque

from ardor.events import GameEvent

from typing import List


class EventConsole:

    def __init__(self, x: int, y: int,
                 width: int=20, height: int=15) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.event_console = tcod.console_new(width, height)
        self.event_messages = deque(maxlen=(self.height - 1))  # type: deque

    def add_events(self, events: List[GameEvent]) -> None:
        for e in events:
            if e.emit:
                self.event_messages.appendleft(str(e))

    def render(self) -> None:
        self.event_console.default_fg = tcod.grey
        self.event_console.default_bg = tcod.black

        for i, ev in enumerate(self.event_messages):
            self.event_console.print_(
                0, self.height - i - 1,
                ev.ljust(20),
                tcod.BKGND_SET, tcod.LEFT
            )

    def blit(self, target: tcod.console.Console) -> None:
        self.event_console.blit(
            0, 0, self.width, self.height,
            target, self.x, self.y)
