from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class Comparable(Protocol):  # noqa: PLW1641
    """
    Based on https://github.com/python/typing/issues/59
    """

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...

    @abstractmethod
    def __lt__(self, other: Comparable) -> bool:
        ...

    def __gt__(self, other: Comparable) -> bool:
        return (not self < other) and self != other

    def __le__(self, other: Comparable) -> bool:
        return self < other or self == other

    def __ge__(self, other: Comparable) -> bool:
        return (not self < other)
