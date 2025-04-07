# TODO: Old Accessor-based table stuff...

# @dataclasses.dataclass
# class BaseTableSpec[T](BaseValueSpec[dict[str, T]]):
#     def _apply(self, input: object, source: Source) -> Value[dict[str, T]]:
#         if not isinstance(input, dict):
#             raise ConfigError(f"not a table: {input!r}", source)
#         return self._apply_table(input, source)
#
#     @abc.abstractmethod
#     def _apply_table(
#         self, inputs: dict[str, object], source: Source
#     ) -> Value[dict[str, T]]: ...
#
#
# @dataclasses.dataclass
# class TableEntriesSpec[T](BaseTableSpec[T]):
#     entry_specs: Mapping[str, Spec[Maybe[T]]]
#
#     def _apply_table(
#         self, inputs: dict[str, object], source: Source
#     ) -> Value[dict[str, T]]:
#         return {
#             key: accessor.apply(input, source[key])
#             for key, accessor in self.entry_accessors.items()
#         }
#
#
# @dataclasses.dataclass
# class TableOfSpec[T](BaseSpec[dict[str, T] | None]):
#     value_spec: _table.Spec[T]
#
#     def apply(self, input: object, source: Source) -> dict[str, T] | None:
#         if input is None:
#             return None
#         if not isinstance(input, dict):
#             raise ConfigError(f"not a table: {input!r}", source)
#         return {
#             key: self.value_spec.apply(value, source[key])
#             for key, value in input.items()
#         }
#
#
# # Spec Short-Hands
#
# table = TableSpec
# table_of = TableOfSpec
