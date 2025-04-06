import contextlib
import types
from collections.abc import Callable, Iterable, Sequence
from typing import Self, overload

import attrs

from liblaf.grapes.timing._time import TimerName

from ._base import TimerRecords
from ._function import TimedFunction
from ._iterable import TimedIterable


@attrs.define
class Timer(
    contextlib.AbstractAsyncContextManager,
    contextlib.AbstractContextManager,
    TimerRecords,
):
    async def __aenter__(self) -> Self:
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
        /,
    ) -> None:
        return self.__exit__(exc_type, exc_value, traceback)

    def __call__[**P, T](self, func: Callable[P, T]) -> TimedFunction[P, T]:
        return TimedFunction(
            func,
            label=self.label,
            timers=self.timers,
            log_level_record=self.log_level_record,
            log_level_summary=self.log_level_summary,
            log_summary_at_exit=self.log_summary_at_exit,
        )

    def __enter__(self) -> Self:
        self._start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
        /,
    ) -> None:
        self._end()
        self.log_record(depth=2)

    def start(self) -> None:
        self._start()

    def end(self, depth: int = 2) -> None:
        self._end()
        self.log_record(depth=depth)


@overload
def timer[T](
    iterable: Iterable[T],
    *,
    depth: int = 0,
    label: str | None = None,
    log_level_record: int | str | None = "DEBUG",
    log_level_summary: int | str | None = "INFO",
    log_summary_at_exit: bool = False,
    timers: Sequence[TimerName | str] = ["perf"],
    total: int | None = None,
) -> TimedIterable[T]: ...
@overload
def timer(
    iterable: None = None,
    *,
    depth: int = 0,
    label: str | None = None,
    log_level_record: int | str | None = "DEBUG",
    log_level_summary: int | str | None = "INFO",
    log_summary_at_exit: bool = False,
    timers: Sequence[TimerName | str] = ["perf"],
    total: None = None,
) -> Timer: ...
def timer[T](
    iterable: Iterable[T] | None = None,
    *,
    depth: int = 0,
    label: str | None = None,
    log_level_record: int | str | None = "DEBUG",
    log_level_summary: int | str | None = "INFO",
    log_summary_at_exit: bool = False,
    timers: Sequence[TimerName | str] = ["perf"],
    total: int | None = None,
) -> TimedIterable[T] | Timer:
    if iterable is not None:
        return TimedIterable(
            iterable=iterable,
            label=label,
            timers=timers,
            depth=depth,
            log_level_record=log_level_record,
            log_level_summary=log_level_summary,
            log_summary_at_exit=log_summary_at_exit,
            total=total,
        )
    return Timer(
        label=label,
        timers=timers,
        depth=depth,
        log_level_record=log_level_record,
        log_level_summary=log_level_summary,
        log_summary_at_exit=log_summary_at_exit,
    )
