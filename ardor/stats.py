from ardor.util import clamp


class Stats:

    def __init__(self, hp: int) -> None:
        self.max_hp = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp) -> None:
        self._hp = clamp(hp, 0, self.max_hp)
