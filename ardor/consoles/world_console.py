import tcod
import random
import numpy as np

from .console import Console

from ardor.map import Map
from ardor.entity import Entity, Battler, Stairs
from ardor.player import Player
from ardor.item import ItemEntity
from ardor.colors import (
    DARK_WALL, DARK_GROUND,
    LIGHT_GROUND, LIGHT_WALL
)

from typing import Optional, List, Union  # noqa


TORCH_RADIUS = 5


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

        self.down_stairs = [Stairs(x, y) for x, y, in self.map.stair_locations]

        self.light_walls = True

        self.nothing = np.full(self.map.grid.shape + (3,), tcod.black,
                               dtype=np.uint8)
        self.discovered = np.full(self.map.grid.shape, False,
                                  dtype=np.bool_)

        self.entities = []  # type: List[Entity]
        self.entity_grid = np.empty(self.map.grid.shape, dtype=object)
        for i in self.entity_grid:
            for j in range(len(i)):
                i[j] = []

        for e in self.down_stairs:
            self.add_entity(e)

    def add_entity(self, entity: Entity) -> None:
        self.entities.append(entity)
        self.entity_grid[entity.y][entity.x].append(entity)

    def remove_entity(self, entity: Entity) -> None:
        self.entities.remove(entity)
        self.entity_grid[entity.y][entity.x].remove(entity)

    def get_stairs(self, x: int, y: int) -> Optional[Stairs]:
        ents = list(
            filter(lambda x: isinstance(x, Stairs), self.entity_grid[y][x])
        )

        if len(ents) == 0:
            return None

        return random.choice(ents)

    def get_battler(self, x: int, y: int) -> Optional[Battler]:
        ents = list(
            filter(lambda x: isinstance(x, Battler), self.entity_grid[y][x])
        )

        if len(ents) == 0:
            return None

        return random.choice(ents)

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

            self.discovered = np.logical_or(
                self.map.map.fov, self.discovered)

        where_discovered = np.where(self.discovered)
        where_fov = np.where(self.map.map.fov[:])

        self.console.bg[where_discovered] = self.dark_map_bg[where_discovered]
        self.console.bg[where_fov] = self.light_map_bg[where_fov]

        self.console.ch[np.where(self.map.grid == '=')] = tcod.CHAR_DHLINE
        self.console.fg[np.where(self.map.grid == '=')] = tcod.black

        for e in self.entities:
            if self.map.map.fov[e.y][e.x]:
                e.lit = True
                e.draw(self.console)
            else:
                e.lit = False

        self.player.draw(self.console)

    def is_walkable(self, dest_x: int, dest_y: int) -> Union[bool, Entity]:
        for e in self.entities:
            if e.walkable:
                continue

            if e.x == dest_x and e.y == dest_y:
                return e

        return bool(self.map.map.walkable[dest_y][dest_x])
