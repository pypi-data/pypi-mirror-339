from collections.abc import Callable
from pathlib import Path

from rich.style import Style
from rich.text import Text


def func(obj: Callable) -> Text:
    text = Text()
    file: Path = Path(obj.__code__.co_filename)
    if file.exists():
        text.append(obj.__module__, style=Style(link=file.as_uri()))
        text.append(".")
        text.append(
            f"{obj.__qualname__}(...)",
            style=Style(link=f"{file.as_uri()}#{obj.__code__.co_firstlineno}"),
        )
    else:
        text.append(f"{obj.__module__}.{obj.__qualname__}(...)")
    return text
