from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

_TTagName = str


@dataclass(frozen=True)
class ComponentDependencyInfo:
    tag_name: _TTagName = field(hash=True)
    esm: Path = field(hash=False)
    externals: Optional[List[Path]] = field(
        default_factory=list, compare=False, hash=False
    )
    css: List[Path] = field(default_factory=list, compare=False, hash=False)
