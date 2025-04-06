from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import chain, count, repeat
from typing import cast

from toolz.itertoolz import sliding_window

from .seq import iter_to_seq
from .typing import Comparable


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


def is_sorted[T](
    seq: Iterable[T],
    *,
    key: Callable[[T], Comparable] | None = None,
    reverse: bool = False,
) -> bool:
    local_key: Callable[[T], Comparable]
    if key is None:
        def default_key(v: T) -> Comparable:
            return cast("Comparable", v)

        local_key = default_key
    else:
        local_key = key

    return all(
        (
            local_key(prev) >= local_key(curr) if reverse
            else local_key(prev) <= local_key(curr)
        )
        for prev, curr in sliding_window(2, seq)
    )


def filter_by_positions[T](poss: Iterable[int], seq: Iterable[T]) -> Iterable[T]:
    p: Iterator[int] = iter(poss)

    pos: int | None = next(p, None)
    if pos is None:
        return

    for i, v in enumerate(seq):
        if i == pos:
            yield v

            pos = next(p, None)
            if pos is None:
                return


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


def remap[KT, VT](
    data: Iterable[KT],
    mapping: dict[KT, VT],
    *,
    key: Callable[[KT], VT] | None = None,
) -> Iterable[VT]:
    local_key: Callable[[KT], VT]
    if key is None:
        c = count(start=0)

        def default_key(_: KT) -> VT:
            return cast("VT", next(c))

        local_key = default_key
    else:
        local_key = key

    k: KT
    for k in data:
        yield mapping.setdefault(k, local_key(k))
