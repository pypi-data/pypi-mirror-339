from collections.abc import Callable, Iterable, Sequence


def iter_to_seq[T](
    a: Iterable[T],
    target: Callable[[Iterable[T]], Sequence[T]] = tuple,
) -> Sequence[T]:
    if isinstance(a, Sequence):
        return a

    return target(a)
