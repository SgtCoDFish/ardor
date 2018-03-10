from ardor.util import clamp


class Stats:

    def __init__(self, max_hp: int, max_cap: float,
                 attack: int, defence: int,
                 intelligence: int, spirit: int) -> None:
        self.max_hp = max_hp
        self._hp = self.max_hp

        self.max_cap = max_cap
        self._cap = self.max_cap / 2.0

        self.attack = attack
        self.defence = defence
        self.intelligence = intelligence
        self.spirit = spirit

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, hp) -> None:
        self._hp = clamp(hp, 0, self.max_hp)

    @property
    def cap(self) -> float:
        return self._cap

    @cap.setter
    def cap(self, cap) -> None:
        self._cap = clamp(cap, 0.0, self.max_cap)
