import tcod

from .console import Console

from collections import deque
from ardor.events import GameEvent

from typing import List


def split_msg(msg: str, width: int) -> List[str]:
    split_msgs = msg.split(" ")
    out = []  # type: List[str]

    tmps = ""

    while True:
        if len(split_msgs) == 0:
            out.append(tmps)
            break

        work = split_msgs[0]
        split_msgs = split_msgs[1:]

        if len(work) > width:
            # if an individual word is too long, we have to break
            # or we'll infinitely loop
            print("WARNING: Super long message:", msg)
            return ["very long message"]

        if len(tmps) == 0:
            candidate = work
        else:
            candidate = tmps + " " + work

        if len(candidate) > width:
            out.append(tmps)
            tmps = work
        else:
            tmps = candidate

    return out


class EventConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        super().__init__(x, y, width, height)
        self.event_messages = deque(maxlen=(self.height - 1))  # type: deque

    def add_events(self, events: List[GameEvent]) -> None:
        for e in events:
            if e.emit:
                full_msg = str(e)
                if len(full_msg) >= self.width:
                    msgs = split_msg(full_msg, self.width)
                else:
                    msgs = [full_msg]

                for m in msgs:
                    self.event_messages.appendleft(m)

    def render(self) -> None:
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black

        for i, ev in enumerate(self.event_messages):
            self.console.print_(
                0, self.height - i - 1,
                ev.ljust(self.width),
                tcod.BKGND_SET, tcod.LEFT
            )
