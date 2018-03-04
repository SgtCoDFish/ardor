import tcod
import numpy as np

from typing import List


class Map:

    def __init__(self, width: int, height: int,
                 layout: List[str]) -> None:
        self.width = width
        self.height = height
        self.layout = layout
        self.grid = np.array([list(line) for line in layout])

        self.map = tcod.map_new(self.width, self.height)

        self.map.walkable[:] = self.grid[:] == ' '
        self.map.transparent[:] = self.map.walkable[:] | (self.grid == '=')
