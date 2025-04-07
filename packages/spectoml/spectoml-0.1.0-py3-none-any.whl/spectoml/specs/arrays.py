from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Never, override

from specs._util import ArgUnset as _ArgUnset
from specs.base import BaseValueSpec, ValueSpec
from specs.errors import SpecError
from specs.source import Source
from specs.value import Value


class ArraySpec(BaseValueSpec[list[object]]):
    @override
    def apply(self, input: Value[object], source: Source) -> Value[list[object]]:
        value = input.value
        if not isinstance(value, list):
            raise SpecError(f"not an array: {value!r}", source)
        return Value(value)

    def empty(self) -> ValueSpec[list[Never]]:
        return self.also(EmptyArraySpec())

    def of[T](
        self,
        item_spec: ValueSpec[T],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> ValueSpec[list[T]]:
        return self.also(
            ArrayOfSpec(item_spec, min_length=min_length, max_length=max_length)
        )

    def with_items[T](
        self,
        *item_specs: ValueSpec[T],
        rest_spec: ValueSpec[Sequence[T], list[object]]
        | _ArgUnset = _ArgUnset.SENTINEL,
    ) -> ValueSpec[list[T]]:
        if rest_spec is _ArgUnset.SENTINEL:
            return self.also(ArrayWithItemsSpec(item_specs))
        return self.also(ArrayWithItemsSpec(item_specs, rest_spec))


array = ArraySpec


@dataclass
class EmptyArraySpec(BaseValueSpec[list[Never], list[object]]):
    @override
    def apply(
        self, input: Value[Sequence[object]], source: Source
    ) -> Value[list[Never]]:
        values = input.value
        if values:
            raise SpecError(
                f"expected an empty array, found {len(values)} items", source
            )
        return Value([])


@dataclass
class ArrayOfSpec[T](BaseValueSpec[list[T], list[object]]):
    item_spec: ValueSpec[T]
    min_length: int | None = field(default=None, kw_only=True)
    max_length: int | None = field(default=None, kw_only=True)

    @override
    def apply(self, input: Value[list[object]], source: Source) -> Value[list[T]]:
        values = input.value
        if self.min_length is not None and len(values) < self.min_length:
            raise SpecError(
                f"expected at least {self.min_length} array item(s), found {len(values)} item(s)",
                source,
            )
        if self.max_length is not None and len(values) > self.max_length:
            raise SpecError(
                f"expected at most {self.max_length} array item(s), found: {len(values)} item(s)",
                source,
            )
        return Value(
            [
                self.item_spec.apply(Value(input), source[index]).value
                for index, input in enumerate(values)
            ]
        )


@dataclass
class ArrayWithItemsSpec[T](BaseValueSpec[list[T], list[object]]):
    item_specs: Sequence[ValueSpec[T]]
    rest_spec: ValueSpec[Sequence[T], list[object]] = EmptyArraySpec()

    @override
    def apply(self, input: Value[list[object]], source: Source) -> Value[list[T]]:
        values = input.value

        item_specs_len = len(self.item_specs)
        if len(values) < item_specs_len:
            raise SpecError(
                f"expected at least {item_specs_len} items, found {len(values)} item(s)",
                source[:item_specs_len],
            )

        item_inputs = [Value(input) for input in values[:item_specs_len]]
        rest_input = Value([input for input in values[item_specs_len:]])

        items = (
            spec.apply(input, source[index]).value
            for index, (spec, input) in enumerate(zip(self.item_specs, item_inputs))
        )

        rest = self.rest_spec.apply(rest_input, source[len(self.item_specs) :]).value

        return Value([*items, *rest])
