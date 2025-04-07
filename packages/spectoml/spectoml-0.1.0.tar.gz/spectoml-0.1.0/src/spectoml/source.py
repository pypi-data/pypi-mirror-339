from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass(frozen=True)
class KeyPath:
    type Key = (
        str
        | int
        | slice[int, int, None]
        | slice[int, None, None]
        | slice[None, int, None]
    )

    type Path = tuple[KeyPath.Segment, ...]
    type PathLike = Sequence[KeyPath.Segment]

    @dataclass(frozen=True)
    class Segment:
        key: KeyPath.Key

        def __str__(self) -> str:
            match self.key:
                case slice(start=int(start), stop=int(stop)):
                    return f"[{start}:{stop}]"
                case slice(start=int(start)):
                    return f"[{start}:]"
                case slice(stop=int(stop)):
                    return f"[:{stop}]"
                case int(index):
                    return f"[{index}]"
                case str(name):
                    return f".{name}"

    path: KeyPath.Path = ()

    def __getitem__(self, key: KeyPath.Key) -> KeyPath:
        new_path_prefix: KeyPath.PathLike
        new_segment: KeyPath.Segment

        match self.path:
            # If the current path ends in a slice with a non-null start, the new
            # key replaces the slice but adds the slice's offset. We don't
            # enforce the slice's stop/length -- that was just for show.
            case [*path_prefix, KeyPath.Segment(slice(start=int(offset)))]:
                new_path_prefix = path_prefix
                match key:
                    case slice(start=int(start), stop=int(stop)):
                        new_segment = KeyPath.Segment(
                            slice(offset + start, offset + stop)
                        )
                    case slice(start=int(start)):
                        new_segment = KeyPath.Segment(slice(offset + start, None))
                    case slice(stop=int(stop)):
                        new_segment = KeyPath.Segment(slice(None, offset + stop))
                    case int(index):
                        new_segment = KeyPath.Segment(offset + index)
                    case str(name):
                        raise ValueError(
                            f"indexed into a slice with a string key: {self.path!r}, {name!r}"
                        )
            case _:
                new_path_prefix = self.path
                new_segment = KeyPath.Segment(key)

        return replace(self, path=(*new_path_prefix, new_segment))

    def __str__(self) -> str:
        key_path_str = "".join(str(key) for key in self.path)
        return f"<root>{key_path_str}"


@dataclass(frozen=True)
class Source:
    config_file: Path | None = None
    key_path: KeyPath = KeyPath()

    def __getitem__(self, key: KeyPath.Key) -> Source:
        return replace(self, key_path=self.key_path[key])

    def prefix_str(self) -> str:
        if self.config_file:
            file_str = self.config_file
        else:
            file_str = "anonymous config"

        return f"In {file_str} at {self.key_path}:"
