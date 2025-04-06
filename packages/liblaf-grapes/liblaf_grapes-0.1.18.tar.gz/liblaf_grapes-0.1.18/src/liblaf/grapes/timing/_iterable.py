from collections.abc import Iterable, Iterator

import attrs

from ._base import TimerRecords


@attrs.define
class TimedIterable[T](TimerRecords):
    total: int | None = attrs.field(default=None, kw_only=True)
    _iterable: Iterable[T] = attrs.field(
        alias="iterable", on_setattr=attrs.setters.frozen
    )

    def __attrs_post_init__(self) -> None:
        self.label = self.label or "Iterable"

    def __contains__(self, x: object, /) -> bool:
        return x in self._iterable  # pyright: ignore[reportOperatorIssue]

    def __iter__(self) -> Iterator[T]:
        for item in self._iterable:
            self._start()
            yield item
            self._end()
            self.log_record(depth=2)
        self.log_summary(depth=2)

    def __len__(self) -> int:
        if self.total is not None:
            return self.total
        return len(self._iterable)  # pyright: ignore[reportArgumentType]
