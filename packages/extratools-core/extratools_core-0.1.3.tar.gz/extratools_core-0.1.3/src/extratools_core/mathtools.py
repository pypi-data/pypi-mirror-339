from collections import Counter
from collections.abc import Iterable
from math import inf, log2


def safediv(a: float, b: float) -> float:
    return inf * a if b == 0 else a / b


def entropy[T](data: Iterable[T]) -> float:
    counter: Counter[T] = Counter(data)
    total: int = sum(counter.values())

    return -sum(
        p * log2(p)
        for p in (
            curr / total
            for curr in counter.values()
        )
    )
