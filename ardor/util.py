from typing import TypeVar

N = TypeVar("N", int, float)


def clamp(n: int, smallest: N, largest: N) -> N:
    return max(smallest, min(n, largest))
