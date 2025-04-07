from __future__ import annotations

from .source import Source


class SpecError(Exception):
    def __init__(
        self,
        message: str,
        source: Source | None = None,
    ) -> None:
        self.message: str = message
        self.source: Source | None = source

    def __str__(self) -> str:
        if self.source is None:
            return self.message

        return f"{self.source.prefix_str()}: {self.message}"
