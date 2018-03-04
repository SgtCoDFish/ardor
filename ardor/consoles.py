import abc
import tcod

import numpy as np

from collections import deque

from ardor.map import Map
from ardor.events import GameEvent
from ardor.player import Player

from typing import List


DARK_WALL = tcod.Color(0, 0, 100)
LIGHT_WALL = tcod.Color(130, 110, 50)
DARK_GROUND = tcod.Color(50, 50, 150)
LIGHT_GROUND = tcod.Color(200, 180, 50)

TORCH_RADIUS = 4
SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS


class Console(abc.ABC):

    def __init__(self, x: int, y: int,
                 width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.console = tcod.console_new(self.width, self.height)

    @abc.abstractmethod
    def render(self) -> None:
        pass

    def blit(self, target: tcod.console.Console) -> None:
        self.console.blit(
            0, 0, self.width, self.height,
            target, self.x, self.y)

    def clear(self) -> None:
        tcod.console_clear(self.console)


class EventConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int=20, height: int=15) -> None:
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
                ev.ljust(20),
                tcod.BKGND_SET, tcod.LEFT
            )


class WorldConsole(Console):

    def __init__(self, x: int, y: int, world_map: Map, player: Player):
        super().__init__(x, y, world_map.width, world_map.height)
        self.player = player
        self.map = world_map
        self.recompute_lighting = True

        self.light_map_bg = np.full(self.map.grid.shape + (3,), LIGHT_GROUND,
                                    dtype=np.uint8)
        self.light_map_bg[self.map.grid[:] == '#'] = LIGHT_WALL
        self.dark_map_bg = np.full(self.map.grid.shape + (3,), DARK_GROUND,
                                   dtype=np.uint8)
        self.dark_map_bg[self.map.grid[:] == '#'] = DARK_WALL

        self.light_walls = True

        # 1d noise for the torch flickering
        self.noise = tcod.noise_new(1, 1.0, 1.0)
        self.torchx = 0.0

    def render(self) -> None:
        # self.clear()

        dx = 0.0
        dy = 0.0
        di = 0.0

        if self.recompute_lighting:
            self.recompute_lighting = False
            self.map.map.compute_fov(
                self.player.x,
                self.player.y,
                TORCH_RADIUS if self.player.torch else 0,
                self.light_walls,
                tcod.FOV_SHADOW
            )
            self.console.bg[:] = self.dark_map_bg[:]
            if self.player.torch:
                # slightly change the perlin noise parameter
                self.torchx += 0.1
                # randomize the light position between -1.5 and 1.5
                tdx = [self.torchx + 20.0]
                dx = tcod.noise_get(self.noise, tdx, tcod.NOISE_SIMPLEX) * 1.5
                tdx[0] += 30.0
                dy = tcod.noise_get(self.noise, tdx, tcod.NOISE_SIMPLEX) * 1.5
                di = 0.2 * tcod.noise_get(
                    self.noise, [self.torchx], tcod.NOISE_SIMPLEX
                )
                print(self.map.width, self.map.height)
                print(self.player.x, self.player.y)

                mgrid = np.mgrid[:self.map.width, :self.map.height]
                # get squared distance
                light = ((mgrid[0] - self.player.y + dy) ** 2 +
                         (mgrid[1] - self.player.x + dx) ** 2)
                light = light.astype(np.float16)
                print("light:", light)
                where_visible = np.where((light < SQUARED_TORCH_RADIUS) &
                                         self.map.map.fov[:])
                light[where_visible] = (
                    SQUARED_TORCH_RADIUS - light[where_visible]
                )
                light[where_visible] /= SQUARED_TORCH_RADIUS
                light[where_visible] += di
                light[where_visible] = light[where_visible].clip(0, 1)

                for yx in zip(*where_visible):
                    self.world_console.console.bg[yx] = tcod.color_lerp(
                        tuple(self.dark_map_bg[yx]),
                        tuple(self.light_map_bg[yx]),
                        light[yx],
                    )
        else:
            where_fov = np.where(self.map.map.fov[:])
            self.console.bg[where_fov] = \
                self.light_map_bg[where_fov]

        self.console.ch[np.where(self.map.grid == '=')] = tcod.CHAR_DHLINE
        self.console.fg[np.where(self.map.grid == '=')] = tcod.black
