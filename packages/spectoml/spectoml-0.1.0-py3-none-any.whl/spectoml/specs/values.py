from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Never, override

from specs.base import BaseSpec, Spec
from specs.errors import SpecError
from specs.source import Source
from specs.value import Value

type ValueSpec[T, S = object] = Spec[Value[T], Value[S]]


class BaseValueSpec[T, S = object](BaseSpec[Value[T], Value[S]]):
    pass


@dataclass
class NeverSpec(BaseValueSpec[Never]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[Never]:
        raise SpecError(f"expected no value but found: {input!r}", source)


never = NeverSpec


@dataclass
class UnknownSpec(BaseValueSpec[object]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[object]:
        return input


unknown = UnknownSpec


@dataclass
class StringSpec(BaseValueSpec[str]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[str]:
        value = input.value
        if not isinstance(value, str):
            raise SpecError(f"not a string: {value!r}", source)
        return Value(value)

    def enum[E: Enum](self, enum_type: type[E]) -> ValueSpec[E]:
        return self.also(EnumSpec(enum_type))

    def path(self, *, must_exist: bool = False) -> ValueSpec[Path]:
        return self.also(PathSpec(must_exist=must_exist))


string = StringSpec


@dataclass
class IntegerSpec(BaseValueSpec[int]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[int]:
        value = input.value
        if not isinstance(value, int):
            raise SpecError(f"not an integer: {value!r}", source)
        return Value(value)

    def enum[E: Enum](self, enum_type: type[E]) -> ValueSpec[E]:
        return self.also(EnumSpec(enum_type))


integer = IntegerSpec


@dataclass
class BooleanSpec(BaseValueSpec[bool]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[bool]:
        value = input.value
        if not isinstance(value, bool):
            raise SpecError(f"not a boolean: {value!r}", source)
        return Value(value)


boolean = BooleanSpec


@dataclass
class EnumSpec[E: Enum](BaseValueSpec[E]):
    enum_type: type[E]

    @override
    def apply(self, input: Value[object], source: Source) -> Value[E]:
        value = input.value
        if value not in self.enum_type:
            options_str = ", ".join(str(instance.value) for instance in self.enum_type)
            raise SpecError(
                f"not a valid option: {value!r} (expected one of: {options_str})",
                source,
            )
        return Value(self.enum_type(value))


enum = EnumSpec


@dataclass
class PathSpec(BaseValueSpec[Path, str]):
    must_exist: bool = field(default=False, kw_only=True)

    @override
    def apply(self, input: Value[str], source: Source) -> Value[Path]:
        path = Path(input.value)
        if self.must_exist and not path.exists():
            raise SpecError(f"path does not exist: {path}", source)
        return Value(path)


path = PathSpec
