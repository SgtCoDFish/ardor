import tcod


class Map:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.map = tcod.map_new(self.width, self.height)
