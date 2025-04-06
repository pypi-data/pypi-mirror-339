import logging
from collections.abc import Sequence

import loguru

from ._icecream import init_icecream
from ._init_loguru import init_loguru


def init_logging(
    level: int | str = logging.NOTSET,
    *,
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
) -> None:
    init_loguru(level=level, handlers=handlers, levels=levels)
    init_icecream()
