from collections.abc import Callable, Iterable
from io import StringIO
from itertools import zip_longest
from typing import cast

from toolz import sliding_window

from .typing import Comparable


def sorted_to_str[T](
    seq: Iterable[T],
    *,
    key: Callable[[T], Comparable] | None = None,
) -> str:
    def default_key(v: T) -> Comparable:
        return cast("Comparable", v)

    local_key: Callable[[T], Comparable] = default_key if key is None else key

    s = StringIO()

    first: bool = True
    for prev, curr in sliding_window(2, seq):
        if first:
            s.write(repr(prev))
            first = False

        s.write(" == " if local_key(prev) == local_key(curr) else " < ")
        s.write(repr(curr))

    return s.getvalue()


def alignment_to_str[T](
    *seqs: Iterable[T | None],
    default: str = "",
    separator: str = " | ",
) -> str:
    strs: list[StringIO] = []

    for i, col in enumerate(zip_longest(*seqs, fillvalue=default)):
        if i == 0:
            strs = [StringIO() for _ in col]
        else:
            for s in strs:
                s.write(separator)

        vals: list[str] = [
            default if v is None else repr(v)
            for v in col
        ]
        max_len: int = max(
            len(val)
            for val in vals
        )
        pads: list[str] = [
            (max_len - len(val)) * ' '
            for val in vals
        ]

        for s, pad, val in zip(strs, pads, vals, strict=True):
            s.write(val)
            s.write(pad)

    return '\n'.join([s.getvalue() for s in strs])
