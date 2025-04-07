from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol

from specs.base import Spec
from specs.value import Maybe, Value


class KeyedSpec[R: Maybe, I: Maybe[Mapping] = Maybe[Mapping[str, object]]](
    Spec[R, I], Protocol
):
    def keys(self) -> set[str]: ...


type KeyedValueSpec[T] = KeyedSpec[Value[T], Value[Mapping[str, object]]]


# TODO: Old Accessor stuff...

# @dataclasses.dataclass
# class FieldAccessor[T](BaseAccessor[T]):
#     key: str
#     spec: _table.Spec[T]
#
#     def keys(self) -> set[str]:
#         return {self.key}
#
#     def apply(self, inputs: Mapping[str, object], source: Source) -> T:
#         return self.spec.apply(inputs.get(self.key), source)
#
#
# @dataclasses.dataclass
# class FirstOfAccessor[T](BaseAccessor[T | None]):
#     specs: Mapping[str, _table.Spec[T | None]]
#
#     def keys(self) -> set[str]:
#         return set(self.specs.keys())
#
#     def apply(self, inputs: Mapping[str, object], source: Source) -> T | None:
#         values = {
#             key: spec.apply(inputs.get(key), source[key])
#             for key, spec in self.specs.items()
#         }
#         available = {key: value for key, value in values.items() if value is not None}
#
#         if not available:
#             return None
#
#         value, *_ = available.values()
#         return value
#
#
# @dataclasses.dataclass
# class SingleOneOfAccessor[T](BaseAccessor[T | None]):
#     specs: Mapping[str, _table.Spec[T | None]]
#
#     def keys(self) -> set[str]:
#         return set(self.specs.keys())
#
#     def apply(self, inputs: Mapping[str, object], source: Source) -> T | None:
#         values = {
#             key: spec.apply(inputs.get(key), source[key])
#             for key, spec in self.specs.items()
#         }
#         available = {key: value for key, value in values.items() if value is not None}
#
#         if not available:
#             return None
#
#         if len(available) > 1:
#             keys = available.keys()
#             raise ConfigError(f"conflicting keys: {', '.join(keys)}", source=source)
#
#         value, *_ = available.values()
#         return value
#
#
# class ConfigDictAccessor(BaseAccessor[object]):
#     accessors: Mapping[str, _table.Accessor[object]]
#     ignore_extra: bool = False
#
#     def keys(self) -> set[str]:
#         return set.union(*(accessor.keys() for accessor in self.accessors.values()))
#
#
# # Accessor Short-Hands
#
# field = FieldAccessor
# first_of = FirstOfAccessor
# single_one_of = SingleOneOfAccessor
