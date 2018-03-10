import abc

from enum import Enum

from ardor.entity import Battler

from typing import Dict  # noqa


class DamageType(Enum):
    PHYSICAL = 1
    SPECIAL = 2


class Attack(abc.ABC):

    max_range = 0
    pretty = "unknown"

    def __init__(self, attacker: Battler, target: Battler) -> None:
        self.attacker = attacker
        self.target = target


class MeleeAttack(Attack):

    max_range = 1
    pretty = "melee"
    damage_type = DamageType.PHYSICAL


class CapBlastAttack(Attack):

    max_range = 5
    pretty = "cap blast"
    damage_type = DamageType.SPECIAL
