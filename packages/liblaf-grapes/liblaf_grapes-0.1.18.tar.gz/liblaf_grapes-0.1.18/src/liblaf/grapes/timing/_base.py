import atexit
import collections
import statistics
import textwrap
from collections.abc import Generator, Mapping, Sequence
from typing import overload

import attrs
from loguru import logger

from liblaf import grapes

from ._time import TimerName, get_time


@attrs.define
class TimerConfig:
    label: str | None = attrs.field(default=None, kw_only=True)
    timers: Sequence[TimerName | str] = attrs.field(
        factory=lambda: ["perf"], kw_only=True, on_setattr=attrs.setters.frozen
    )

    @property
    def default_timer(self) -> str:
        return self.timers[0]


@attrs.define
class BaseTimer(TimerConfig):
    _time_start: dict[str, float] = attrs.field(
        init=False, factory=dict, on_setattr=attrs.setters.frozen
    )
    _time_end: dict[str, float] = attrs.field(
        init=False, factory=dict, on_setattr=attrs.setters.frozen
    )

    def current_time(self, timer: str | None = None) -> float:
        timer = timer or self.default_timer
        return self._time_end[timer] - self._time_start[timer]

    def _start(self) -> None:
        for timer in self.timers:
            self._time_start[timer] = get_time(timer)

    def _end(self) -> None:
        for timer in self.timers:
            self._time_end[timer] = get_time(timer)

    @property
    def _current_record(self) -> Mapping[str, float]:
        return {
            timer: self._time_end[timer] - self._time_start[timer]
            for timer in self.timers
        }


@attrs.define
class TimerRecords(BaseTimer):
    depth: int = attrs.field(default=0, kw_only=True)
    log_level_record: int | str | None = attrs.field(default="DEBUG", kw_only=True)
    log_level_summary: int | str | None = attrs.field(default="INFO", kw_only=True)
    log_summary_at_exit: bool = attrs.field(default=False, kw_only=True)
    _records: dict[str, list[float]] = attrs.field(
        init=False,
        factory=lambda: collections.defaultdict(list),
        on_setattr=attrs.setters.frozen,
    )

    def __post_attrs_init__(self) -> None:
        if self.log_summary_at_exit:
            register_timer_at_exit(self)

    @overload
    def __getitem__(self, index: int) -> Mapping[str, float]: ...
    @overload
    def __getitem__(self, index: str) -> Sequence[float]: ...
    def __getitem__(self, index: int | str) -> Mapping[str, float] | Sequence[float]:
        if isinstance(index, int):
            return self.row(index)
        return self.column(index)

    def __len__(self) -> int:
        return self.count

    @property
    def columns(self) -> Sequence[str]:
        return self.timers

    @property
    def count(self) -> int:
        return self.n_rows

    @property
    def n_columns(self) -> int:
        return len(self.timers)

    @property
    def n_rows(self) -> int:
        return len(self.column())

    def column(self, timer: str | None = None) -> Sequence[float]:
        timer = timer or self.default_timer
        return self._records[timer]

    def human_record(self, index: int = -1, label: str | None = None) -> str:
        label = label or self.label or "Timer"
        text: str = f"{label} > "
        items: list[str] = []
        for timer, value in self.row(index).items():
            human_duration: str = grapes.human_duration(value)
            items.append(f"{timer}: {human_duration}")
        text += ", ".join(items)
        return text

    def human_summary(self, label: str | None = None) -> str:
        label = label or self.label or "Timer"
        header: str = f"{label} (total: {self.n_rows})"
        if self.n_rows == 0:
            return header
        body: str = ""
        for timer in self.columns:
            body += f"{timer} > "
            human_mean: str = grapes.human_duration_series(self.column(timer))
            human_median: str = grapes.human_duration(self.median(timer))
            body += f"mean: {human_mean}, median: {human_median}\n"
        body = body.strip()
        summary: str = header + "\n" + textwrap.indent(body, "  ")
        return summary

    def iter_columns(self) -> Generator[tuple[str, Sequence[float]]]:
        yield from self._records.items()

    def iter_rows(self) -> Generator[Mapping[str, float]]:
        for index in range(self.n_rows):
            yield self.row(index)

    def log_record(
        self,
        index: int = -1,
        label: str | None = None,
        depth: int = 1,
        level: int | str | None = None,
    ) -> None:
        level = level or self.log_level_record
        if level is None:
            return
        logger.opt(depth=self.depth + depth).log(
            level, self.human_record(index=index, label=label)
        )

    def log_summary(
        self, label: str | None = None, depth: int = 1, level: int | str | None = None
    ) -> None:
        level = level or self.log_level_summary
        if level is None:
            return
        logger.opt(depth=self.depth + depth).log(level, self.human_summary(label=label))

    def row(self, index: int) -> Mapping[str, float]:
        return {timer: values[index] for timer, values in self._records.items()}

    # region statistics

    def max(self, timer: str | None = None) -> float:
        return max(self.column(timer))

    def mean(self, timer: str | None = None) -> float:
        return statistics.mean(self.column(timer))

    def median(self, timer: str | None = None) -> float:
        return statistics.median(self.column(timer))

    def min(self, timer: str | None = None) -> float:
        return min(self.column(timer))

    def std(self, timer: str | None = None) -> float:
        return statistics.stdev(self.column(timer))

    # endregion statistics

    def _append(
        self, seconds: Mapping[str, float] = {}, nanoseconds: Mapping[str, float] = {}
    ) -> None:
        for key, value in seconds.items():
            self._records[key].append(value)
        for key, value in nanoseconds.items():
            self._records[key].append(value * 1e-9)

    def _end(self) -> None:
        super()._end()
        self._append(seconds=self._current_record)


TIMERS: list[TimerRecords] = []


def register_timer_at_exit(timer: TimerRecords) -> None:
    TIMERS.append(timer)


def log_summary() -> None:
    for timer in TIMERS:
        if timer.log_summary_at_exit and timer.n_rows > 1:
            timer.log_summary()


atexit.register(log_summary)
