from __future__ import annotations

import dataclasses
import pathlib

from .folder import Folder


@dataclasses.dataclass
class Workspace:
    folder: Folder | None = None
