import os
from pathlib import Path

from rich.style import Style
from rich.text import Text


def location(
    name: str | None,
    function: str | None,
    line: int | None,
    file: str | os.PathLike[str] | None = None,
) -> Text:
    text = Text()
    file: Path | None = Path(file or "<unknown>")
    function = function or "<unknown>"
    line = line or 0
    if file.exists():
        text.append(str(name), style=Style(link=file.as_uri()))
        text.append(":")
        text.append(f"{function}:{line}", style=Style(link=f"{file.as_uri()}#{line}"))
    else:
        text.append(f"{name}:{function}:{line}")
    return text
