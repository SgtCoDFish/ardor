import random

from ardor.ai import AIType
from ardor.entity import Battler
from ardor.stats import Stats
from ardor.attack import Attack, MeleeAttack
from ardor.inventory import Inventory

from typing import Optional


class Mob(Battler):

    def __init__(self, initial_x: int, initial_y: int,
                 symbol: str, stats: Stats,
                 ai_type: AIType) -> None:
        super().__init__(initial_x, initial_y, symbol, stats)

        self.inventory = Inventory(5.0)

        self.ai_type = ai_type

        self.attack_types = [MeleeAttack]

    def do_attack(self, target: Battler) -> Optional[Attack]:
        dist = self.distance_to(target)

        valid_attacks = list(filter(lambda x: dist <= x.max_range,
                                    self.attack_types))

        if len(valid_attacks) == 0:
            return None

        return random.choice(valid_attacks)(self, target)
