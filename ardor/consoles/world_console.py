import tcod
import numpy as np

from .console import Console

from ardor.map import Map
from ardor.entity import Entity
from ardor.player import Player
from ardor.item import ItemEntity

from typing import Optional, List, Union  # noqa


DARK_WALL = tcod.Color(0, 0, 100)
LIGHT_WALL = tcod.Color(130, 110, 50)
DARK_GROUND = tcod.Color(50, 50, 150)
LIGHT_GROUND = tcod.Color(200, 180, 50)

TORCH_RADIUS = 4
SQUARED_TORCH_RADIUS = TORCH_RADIUS * TORCH_RADIUS


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

        self.entities = []  # type: List[Entity]
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
        self.clear()

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

    def is_walkable(self, dest_x: int, dest_y: int) -> Union[bool, Entity]:
        for e in self.entities:
            if e.walkable:
                continue

            if e.x == dest_x and e.y == dest_y:
                return e

        return bool(self.map.map.walkable[dest_y][dest_x])
