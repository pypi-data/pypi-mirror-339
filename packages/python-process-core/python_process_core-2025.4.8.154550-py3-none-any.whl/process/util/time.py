import time
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager
from typing import AnyStr, Generator, NoReturn, Any

from dateutil import parser


def get_local_tz() -> timezone:
    ts = time.localtime()
    td = timedelta(seconds=ts.tm_gmtoff)
    return timezone(offset=td, name=ts.tm_zone)

DEFAULT_TIMEZONE: timezone = get_local_tz()


def parse_datetime(value: str) -> datetime:
    return parser.parse(value)

def timestamp_to_datetime(ts: float, tz: timezone = DEFAULT_TIMEZONE) -> datetime:
    return datetime.fromtimestamp(ts, tz=tz)

def struct_time_to_datetime(struct_time: time.struct_time, tz: timezone = DEFAULT_TIMEZONE) -> datetime:
    ts = time.mktime(struct_time)
    return timestamp_to_datetime(ts, tz=tz)

def timestamped(gen: Generator) -> Generator[tuple[datetime, Any], None, None]:
    """
    Decorator that adds a timestamp to the values yielded by the generator.
    """
    for value in gen:
        yield datetime.now(tz=DEFAULT_TIMEZONE), value
