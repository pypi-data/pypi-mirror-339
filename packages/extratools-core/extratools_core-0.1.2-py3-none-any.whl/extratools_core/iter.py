from collections.abc import Callable, Iterable, Sequence
from itertools import chain, repeat

from toolz.itertoolz import sliding_window

from .seq import iter_to_seq


def iter_to_grams[T](
    _iter: Iterable[T],
    *,
    n: int,
    pad: T | None = None,
) -> Iterable[Sequence[T]]:
    if pad is not None:
        _iter = chain(
            repeat(pad, n - 1),
            _iter,
            repeat(pad, n - 1),
        )

    return sliding_window(n, _iter)


def filter_by_others[T](func: Callable[[T, T], bool], _iter: Iterable[T]) -> Iterable[T]:
    seq: Sequence[T] = iter_to_seq(_iter)

    filtered_ids: set[int] = set(range(len(seq)))

    for i, x in enumerate(seq):
        remove: bool = False
        for j in filtered_ids:
            if i == j:
                continue

            if not func(x, seq[j]):
                remove = True
                break

        if remove:
            filtered_ids.remove(i)

    for i in filtered_ids:
        yield seq[i]
