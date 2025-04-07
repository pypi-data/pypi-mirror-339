from __future__ import annotations

from functools import wraps
from inspect import Parameter, Signature
from typing import Callable, Concatenate


type Transform[T, U] = Callable[Concatenate[T, ...], U]
type NoArgFactory[T] = Callable[[], T]


def handle_kwargs[T, R](
    transform: Transform[T, R], *, keywords: set[str]
) -> Transform[T, R]:
    signature = Signature.from_callable(transform)

    allowed_keywords = set(keywords)
    explicit_keywords: set[str] = set()
    has_kwargs: bool = False

    for i, param in enumerate(signature.parameters.values()):
        match param.kind:
            case Parameter.POSITIONAL_OR_KEYWORD if i == 0:
                # Even if the first parameter *could* be used as a keyword,
                # ignore it if it could be positional. The caller will pass the
                # value argument positionally, which would conflict with a
                # potential keyword parameter.
                allowed_keywords.remove(param.name)
            case Parameter.POSITIONAL_OR_KEYWORD | Parameter.KEYWORD_ONLY:
                # Track any explicit keyword parameters. As long as they aren't
                # also the first positional parameter, they're fair game.
                explicit_keywords.add(param.name)
            case Parameter.VAR_KEYWORD:
                # If the function allows arbitrary keyword arguments, then any
                # keywords that aren't explicitly disallowed are allowed.
                has_kwargs = True

    # If the function does not allow arbitrary keyword arguments, we restrict
    # ourselves to the explicit keyword parameters.
    if not has_kwargs:
        allowed_keywords &= explicit_keywords

    # If the function can handle all the requested keywords as-is, return it
    # directly.
    if keywords <= allowed_keywords:
        return transform

    @wraps(transform)
    def _handle_extra(value: T, /, **kwargs) -> R:
        allowed_kwargs = {keyword: kwargs[keyword] for keyword in allowed_keywords}
        return transform(value, **allowed_kwargs)

    return _handle_extra
