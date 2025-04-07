from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Never, TypeIs, TypeVar


# There's currently a bug/limitation with inferring variance for dataclass field
# type variables.
#
# See:
#   https://github.com/python/mypy/issues/17623
#
_ValueT_co = TypeVar("_ValueT_co", covariant=True)


@dataclass(frozen=True)
class Value(Generic[_ValueT_co]):
    value: _ValueT_co

    def __post_init__(self):
        # Value is meant to be a flat type -- we don't support "meta specs".
        if isinstance(self.value, Value):
            raise TypeError(f"value nested in value: {self!r} (probable logic error?)")
        if isinstance(self.value, Missing):
            raise TypeError(
                f"missing nested in value: {self!r} (probable logic error?)"
            )


@dataclass(frozen=True)
class Missing:
    pass


type MissingPart = Missing | Never
type Maybe[T, M: MissingPart = Missing] = Value[T] | M


def is_value[T](maybe: Maybe[T]) -> TypeIs[Value[T]]:
    return isinstance(maybe, Value)


def is_missing(maybe: Maybe) -> TypeIs[Missing]:
    return isinstance(maybe, Missing)
