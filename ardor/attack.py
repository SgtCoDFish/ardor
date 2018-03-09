import abc

from ardor.entity import Battler

from typing import Dict  # noqa


class Attack(abc.ABC):

    max_range = 0
    pretty = "unknown"

    def __init__(self, attacker: Battler, target: Battler) -> None:
        self.attacker = attacker
        self.target = target


class MeleeAttack(Attack):

    max_range = 1
    pretty = "melee"
    damage = 3


class CapBlastAttack(Attack):

    max_range = 5
    pretty = "cap blast"
    damage = 8
