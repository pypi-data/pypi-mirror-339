from __future__ import annotations

import dataclasses
import pathlib


@dataclasses.dataclass
class Folder:
    path: pathlib.Path
    audio_files: list[pathlib.Path]
