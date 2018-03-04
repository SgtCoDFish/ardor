import abc
import tcod

import numpy as np

from collections import deque

from ardor.map import Map
from ardor.entity import Entity
from ardor.events import GameEvent
from ardor.player import Player
from ardor.item import ItemEntity

from typing import List, Optional


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


class HUDConsole(Console):

    def __init__(self, x: int, y: int,
                 width: int, height: int,
                 target: Entity) -> None:
        super().__init__(x, y, width, height)
        self.target = target

    def render(self) -> None:
        self.console.default_fg = tcod.grey
        self.console.default_bg = tcod.black

        self.console.print_(
            0, 0, "{} HP: {}/{}".format(
                self.target.symbol,
                self.target.stats.hp,
                self.target.stats.max_hp
            ).ljust(self.width), tcod.BKGND_SET, tcod.LEFT
        )


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


class WorldConsole(Console):

    def __init__(self, x: int, y: int, world_map: Map, player: Player) -> None:
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

        self.entities = []  # type: List[GameEntity]
        self.entity_grid = np.empty(self.map.grid.shape, dtype=object)
        for i in self.entity_grid:
            for j in range(len(i)):
                i[j] = []

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)
        self.entity_grid[entity.y][entity.x].append(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)
        self.entity_grid[entity.y][entity.x].remove(entity)

    def pop_item(self, x: int, y: int) -> Optional[ItemEntity]:
        ents = self.entity_grid[y][x]
        if len(ents) == 0:
            return None

        r = next((x for x in ents if isinstance(x, ItemEntity)), None)

        if r is not None:
            self.remove_entity(r)

        return r

    def render(self) -> None:
        # self.clear()

        if self.recompute_lighting:
            self.recompute_lighting = False
            self.map.map.compute_fov(
                self.player.x,
                self.player.y,
                TORCH_RADIUS if self.player.torch else 2,
                self.light_walls,
                tcod.FOV_SHADOW
            )
            self.console.bg[:] = self.dark_map_bg[:]
            where_fov = np.where(self.map.map.fov[:])
            self.console.bg[where_fov] = \
                self.light_map_bg[where_fov]

        self.console.ch[np.where(self.map.grid == '=')] = tcod.CHAR_DHLINE
        self.console.fg[np.where(self.map.grid == '=')] = tcod.black

        for e in self.entities:
            if self.map.map.fov[e.y][e.x]:
                e.lit = True
                e.draw(self.console)
            else:
                e.lit = False
                e.undraw(self.console)

        self.player.draw(self.console)
