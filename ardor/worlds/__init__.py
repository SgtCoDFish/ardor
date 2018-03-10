class World:

    width = -1

    def __init__(self, root_width: int) -> None:
        self.x = root_width - self.width - 1


from .world1 import World1  # noqa
from .world2 import World2  # noqa
from .world3 import World3  # noqa
