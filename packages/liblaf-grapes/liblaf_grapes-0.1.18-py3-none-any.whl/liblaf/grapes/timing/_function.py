import functools
from collections.abc import Callable

import attrs

from liblaf import grapes

from ._base import TimerRecords


# `slots=False` is required to make `functools.update_wrapper(...)` work
# ref: <https://www.attrs.org/en/stable/glossary.html#term-slotted-classes>
@attrs.define(slots=False)
class TimedFunction[**P, T](TimerRecords):
    _func: Callable[P, T] = attrs.field(alias="func", on_setattr=attrs.setters.frozen)

    def __attrs_post_init__(self) -> None:
        self.label = self.label or grapes.pretty.func(self._func).plain or "Function"
        functools.update_wrapper(self, self._func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self._start()
        result: T = self._func(*args, **kwargs)
        self._end()
        self.log_record(depth=2)
        return result
