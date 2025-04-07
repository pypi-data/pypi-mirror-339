from abc import abstractmethod
from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class Comparable(Protocol):  # noqa: PLW1641
    """
    Based on https://github.com/python/typing/issues/59
    """

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...

    @abstractmethod
    def __lt__(self, other: Self) -> bool:
        ...

    def __gt__(self, other: Self) -> bool:
        return (not self < other) and self != other

    def __le__(self, other: Self) -> bool:
        return self < other or self == other

    def __ge__(self, other: Self) -> bool:
        return (not self < other)
