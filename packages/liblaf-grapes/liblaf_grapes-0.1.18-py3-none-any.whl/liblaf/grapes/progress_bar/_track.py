from collections.abc import Generator, Iterable, Sequence

from rich.progress import Progress

from liblaf import grapes

from ._progress import progress


def track[T](
    iterable: Iterable[T],
    *,
    description: str | bool | None = True,
    log_level_record: int | str | None = "DEBUG",
    log_level_summary: int | str | None = "INFO",
    timers: bool | Sequence[grapes.TimerName | str] = ["perf"],
    total: float | None = None,
) -> Generator[T]:
    if description is True:
        description = grapes.caller_location(2).plain
    description = description or ""
    prog: Progress = progress()
    if timers is True:
        timers = ["perf"]
    if total is None:
        total = try_len(iterable)
    if timers:
        iterable: grapes.TimedIterable[T] = grapes.timer(
            iterable,
            depth=2,
            label=description,
            log_level_record=log_level_record,
            log_level_summary=log_level_summary,
            timers=timers,
            total=int(total) if total is not None else None,
        )
        with prog:
            yield from prog.track(iterable, total=total, description=description)
    else:
        with prog:
            yield from prog.track(iterable, total=total, description=description)


def try_len(iterable: Iterable) -> int | None:
    try:
        return len(iterable)  # pyright: ignore[reportArgumentType]
    except TypeError:
        return None
