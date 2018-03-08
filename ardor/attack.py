from enum import Enum
from ardor.entity import Battler

from typing import Dict  # noqa


class AttackType(Enum):

    MELEE = 1


PRETTY_ATTACK = {
    AttackType.MELEE: "melee"
}  # type: Dict[AttackType, str]


class Attack:

    def __init__(self, attack_type: AttackType,
                 attacker: Battler, target: Battler) -> None:
        self.attack_type = attack_type
        self.attacker = attacker
        self.target = target

        self.damage = self._calculate()

    def _calculate(self) -> int:
        return 4

    def pretty(self) -> str:
        return PRETTY_ATTACK.get(self.attack_type, "unknown")
