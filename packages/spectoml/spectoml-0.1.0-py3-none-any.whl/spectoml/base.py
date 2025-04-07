from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, overload, override

from specs._util import ArgUnset as _ArgUnset
from specs.callable import NoArgFactory, Transform, handle_kwargs
from specs.errors import SpecError
from specs.source import Source
from specs.value import Maybe, Missing, MissingPart, Value, is_missing


class Spec[R: Maybe, I: Maybe = Maybe[object]](Protocol):
    def apply(self, input: I, source: Source) -> R: ...

    def also[R2: Maybe, R1: Maybe](
        self: Spec[R1, I], other: Spec[R2, R1]
    ) -> Spec[R2, I]: ...
    def then[T, U, M: MissingPart](
        self: Spec[Maybe[T, M], I], transform: Transform[T, U]
    ) -> Spec[Maybe[U, M], I]: ...

    def required[T](self: Spec[Maybe[T], I]) -> Spec[Value[T], I | Missing]: ...
    def optional[T](self: Spec[Maybe[T], I]) -> Spec[Maybe[T], I | Missing]: ...

    @overload
    def or_else[T, F](
        self: Spec[Maybe[T], I], *, factory: NoArgFactory[F]
    ) -> Spec[Value[T | F], I | Missing]: ...
    @overload
    def or_else[T, F](
        self: Spec[Maybe[T], I], fallback: F
    ) -> Spec[Value[T | F], I | Missing]: ...

    def or_none[T](self: Spec[Maybe[T], I]) -> Spec[Value[T | None], I | Missing]: ...


type ValueSpec[T, S = object] = Spec[Value[T], Value[S]]


class BaseSpec[R: Maybe, I: Maybe = Maybe[object]](Spec[R, I]):
    @override
    def required[T](self: Spec[Maybe[T], I]) -> Spec[Value[T], I | Missing]:
        return RequiredSpec(self)

    @override
    def also[R2: Maybe, R1: Maybe](
        self: Spec[R1, I], other: Spec[R2, R1]
    ) -> Spec[R2, I]:
        return AlsoSpec(self, other)

    @override
    def then[T, U, M: MissingPart](
        self: Spec[Maybe[T, M], I], transform: Transform[T, U]
    ) -> Spec[Maybe[U, M], I]:
        return ThenSpec(self, transform)

    @override
    def optional[T](self: Spec[Maybe[T], I]) -> Spec[Maybe[T], I | Missing]:
        return OptionalSpec(self)

    @overload
    def or_else[T, F](
        self: Spec[Maybe[T], I], *, factory: NoArgFactory[F]
    ) -> Spec[Value[T | F], I | Missing]: ...
    @overload
    def or_else[T, F](
        self: Spec[Maybe[T], I], fallback: F
    ) -> Spec[Value[T | F], I | Missing]: ...

    @override
    def or_else[T, F](
        self: Spec[Maybe[T], I],
        fallback: F | _ArgUnset = _ArgUnset.SENTINEL,
        *,
        factory: NoArgFactory[F] | _ArgUnset = _ArgUnset.SENTINEL,
    ) -> Spec[Value[T | F], I | Missing]:
        if factory is not _ArgUnset.SENTINEL:
            return OrElseFactorySpec(self, factory)
        if fallback is _ArgUnset.SENTINEL:
            raise TypeError("one of fallback or factory is required")
        return OrElseSpec(self, fallback)

    @override
    def or_none[T](self: Spec[Maybe[T], I]) -> Spec[Value[T | None], I | Missing]:
        return OrElseSpec(self, None)


class BaseValueSpec[T, S = object](BaseSpec[Value[T], Value[S]]):
    pass


@dataclass
class OptionalSpec[T, I: Maybe](BaseSpec[Maybe[T], I | Missing]):
    spec: Spec[Maybe[T], I]

    @override
    def apply(self, input: I | Missing, source: Source) -> Maybe[T]:
        if is_missing(input):
            return input
        return self.spec.apply(input, source)


@dataclass
class RequiredSpec[T, I: Maybe](BaseSpec[Value[T], I | Missing]):
    spec: Spec[Maybe[T], I]

    @override
    def apply(self, input: I | Missing, source: Source) -> Value[T]:
        if is_missing(input):
            raise SpecError("required value is missing", source)
        result = self.spec.apply(input, source)
        if is_missing(result):
            raise SpecError("required value is missing", source)
        return result


@dataclass
class AlsoSpec[R2: Maybe, R1: Maybe, I: Maybe](BaseSpec[R2, I]):
    first_spec: Spec[R1, I]
    second_spec: Spec[R2, R1]

    @override
    def apply(self, input: I, source: Source) -> R2:
        first_result = self.first_spec.apply(input, source)
        return self.second_spec.apply(first_result, source)


@dataclass
class ThenSpec[T, U, M: MissingPart, I: Maybe](BaseSpec[Maybe[U, M], I]):
    spec: Spec[Maybe[T, M], I]
    transform: Transform[T, U]

    def __post_init__(self):
        self.transform = handle_kwargs(self.transform, keywords={"source"})

    @override
    def apply(self, input: I, source: Source) -> Maybe[U, M]:
        result = self.spec.apply(input, source)
        if is_missing(result):
            return result
        return Value(self.transform(result.value))


@dataclass
class OrElseSpec[T, F, I: Maybe](BaseSpec[Value[T | F], I | Missing]):
    spec: Spec[Maybe[T], I]
    fallback: F

    @override
    def apply(self, input: I | Missing, source: Source) -> Value[T | F]:
        if is_missing(input):
            return Value(self.fallback)
        result = self.spec.apply(input, source)
        if is_missing(result):
            return Value(self.fallback)
        return result


@dataclass
class OrElseFactorySpec[T, F, I: Maybe](BaseSpec[Value[T | F], I | Missing]):
    spec: Spec[Maybe[T], I]
    fallback_factory: NoArgFactory[F]

    @override
    def apply(self, input: I | Missing, source: Source) -> Value[T | F]:
        if is_missing(input):
            return Value(self.fallback_factory())
        result = self.spec.apply(input, source)
        if is_missing(result):
            return Value(self.fallback_factory())
        return result
