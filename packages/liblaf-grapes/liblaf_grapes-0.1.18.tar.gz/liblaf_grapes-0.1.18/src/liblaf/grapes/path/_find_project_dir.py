import sys
from pathlib import Path


def find_project_dir(start: Path | None = None, name: str = "src") -> Path:
    if start is None:
        start = Path(sys.argv[0])
    start = start.absolute()
    path: Path = Path(start)
    while path.name != name:
        if path.parent == path:
            return start.parent
        path = path.parent
    return path.parent
