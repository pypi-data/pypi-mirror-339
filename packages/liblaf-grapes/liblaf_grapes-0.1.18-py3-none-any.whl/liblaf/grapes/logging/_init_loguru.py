import logging
from collections.abc import Sequence

import loguru
from loguru import logger

from ._clear_handlers import clear_handlers
from ._default import DEFAULT_LEVELS
from ._handler import file_handler, jsonl_handler, rich_handler
from ._intercept import setup_loguru_logging_intercept
from ._level import add_level
from .filter_ import Filter


def init_loguru(
    level: int | str = logging.NOTSET,
    filter_: Filter | None = None,
    handlers: Sequence["loguru.HandlerConfig"] | None = None,
    levels: Sequence["loguru.LevelConfig"] | None = None,
) -> None:
    """Initialize the Loguru logger with specified configurations.

    Args:
        level: The logging level.
        filter_: A filter to apply to the logger.
        handlers: A sequence of handler configurations.
        levels: A sequence of level configurations.
    """
    if handlers is None:
        handlers: list[loguru.HandlerConfig] = [
            rich_handler(level=level, filter_=filter_)
        ]
        handlers.append(file_handler(level=level, filter_=filter_))
        handlers.append(jsonl_handler(level=level, filter_=filter_))
    logger.configure(handlers=handlers)
    for lvl in levels or DEFAULT_LEVELS:
        add_level(**lvl)
    setup_loguru_logging_intercept(level=level)
    clear_handlers()
