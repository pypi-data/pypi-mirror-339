from collections.abc import Sequence

import loguru

from .filter_._composite import filter_all
from .filter_._once import filter_once
from .filter_.typed import Filter

DEFAULT_LEVEL: int | str = "DEBUG"


def default_filter() -> Filter:
    return filter_all(
        {
            "": "INFO",
            "__main__": "TRACE",
            "liblaf": "DEBUG",
        },
        filter_once(),
    )


DEFAULT_LEVELS: Sequence["loguru.LevelConfig"] = [
    {"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}
]
