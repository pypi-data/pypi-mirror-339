from types import FrameType

from loguru._get_frame import get_frame
from rich.text import Text

from liblaf import grapes


def caller_location(depth: int = 1) -> Text:
    """Returns the file name and line number of the caller's location in the code.

    Args:
        depth: The stack depth to inspect.
        markup: If `True`, returns the file name and line number with markup for links.

    Returns:
        The file name and line number of the caller's location. If the frame cannot be retrieved, returns "<unknown>".
    """
    frame: FrameType | None
    try:
        frame = get_frame(depth)  # pyright: ignore[reportAssignmentType]
    except ValueError:
        frame = None
    file: str | None = None
    function: str | None = None
    line: int | None = None
    name: str | None = None
    if frame is not None:
        file = frame.f_code.co_filename
        function = frame.f_code.co_name
        line = frame.f_lineno
        name = frame.f_globals.get("__name__")
    text: Text = grapes.pretty.location(
        function=function, line=line, name=name, file=file
    )
    return text
