import tcod
import numpy as np

from typing import List, Tuple


class Map:

    def __init__(self, width: int, height: int,
                 layout: List[str]) -> None:
        self.width = width
        self.height = height
        self.layout = layout
        self.grid = np.array([list(line) for line in layout])

        self.map = tcod.map_new(self.width, self.height)

        self.map.walkable[:] = (self.grid[:] == ' ') | (self.grid[:] == '<')
        self.map.transparent[:] = self.map.walkable[:] | (self.grid == '=')

        self.stair_locations = []  # type: List[Tuple[int, int]]

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == '<':
                    self.stair_locations.append((x, y))
