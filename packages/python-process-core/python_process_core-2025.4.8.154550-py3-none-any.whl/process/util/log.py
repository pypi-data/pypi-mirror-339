import inspect
import logging
import logging.handlers
import time
import datetime
from typing import Callable, Optional, Iterable, Generator
from pathlib import Path
import json
from contextlib import contextmanager

import colorama


from process.util.time import DEFAULT_TIMEZONE, timestamp_to_datetime


DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FMT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(funcName)s:%(lineno)d - %(message)s'
DEFAULT_LOG_FILE_RETENTION = 14
DEFAULT_LOG_FILE_INTERVAL = 'd'
DEFAULT_LOG_FILE_ROLL_TIME = datetime.time(hour=0, minute=0, second=0, microsecond=0)
DEFAULT_COLOURED_FORE_KEYS = {'levelname'}
DEFAULT_COLOURED_BACK_LEVELS = {logging.CRITICAL, logging.ERROR}

__pkg_root_logger__ = logging.getLogger('logix')
logger = logging.getLogger(__name__)


colorama.init()

class ColouredFormatMixin:
    FORE_COLOUR_MAP: dict[int, str] = {
        logging.DEBUG: colorama.Fore.CYAN,
        logging.INFO: colorama.Fore.GREEN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.MAGENTA,
    }

    BACK_COLOUR_MAP: dict[int, str] = {
        logging.DEBUG: colorama.Back.CYAN,
        logging.INFO: colorama.Back.GREEN,
        logging.WARNING: colorama.Back.YELLOW,
        logging.ERROR: colorama.Back.RED,
        logging.CRITICAL: colorama.Back.MAGENTA,
    }

    def fore_colour_formatter(self, log_level: int) -> Callable[[str], str]:
        ansii_code = self.FORE_COLOUR_MAP.get(log_level)
        return lambda text: f'{ansii_code}{text}{colorama.Fore.RESET}'
    
    def back_colour_formatter(self, log_level: int) -> Callable[[str], str]:
        ansii_code = self.BACK_COLOUR_MAP.get(log_level)
        return lambda text: f'{ansii_code}{text}{colorama.Back.RESET}'


class DateFormatter(logging.Formatter):
    tz: datetime.timezone = DEFAULT_TIMEZONE
    
    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        ts: datetime.datetime = timestamp_to_datetime(record.created, tz=self.tz)
        if datefmt is None:
            return ts.isoformat()
        else:
            return ts.strftime(format=datefmt)

class DefaultStreamStyle(logging.PercentStyle, ColouredFormatMixin):
    def __init__(
        self, 
        fmt: str = DEFAULT_LOG_FMT, 
        defaults: Optional[dict] = None,
        highlight_levels: Optional[set[int]] = DEFAULT_COLOURED_BACK_LEVELS,
        coloured_keys: Optional[set[str]] = DEFAULT_COLOURED_FORE_KEYS
    ) -> None:
        super().__init__(fmt=fmt, defaults=defaults)
        self.highlight_levels = highlight_levels
        self.coloured_keys = coloured_keys

    def _format(self, record: logging.LogRecord) -> str:
        defaults: dict
        if defaults := getattr(self, '_defaults', {}):
            values = defaults | record.__dict__
        else:
            values = record.__dict__.copy()
        if self.highlight_levels and record.levelno in self.highlight_levels:
            return self.back_colour_formatter(log_level=record.levelno)(self._fmt % values)
        elif self.coloured_keys:
            for k in self.coloured_keys:
                if k in values:
                    values[k] = self.fore_colour_formatter(log_level=record.levelno)(values[k])
        return self._fmt % values

class DefaultStreamFormatter(ColouredFormatMixin, DateFormatter):
    def __init__(
        self, 
        fmt: str = DEFAULT_LOG_FMT,
        datefmt: Optional[str] = None,
        validate: bool = True,
        coloured_keys: Optional[set[str]] = DEFAULT_COLOURED_FORE_KEYS,
        defaults: Optional[dict] = None,
        tz: datetime.timezone = DEFAULT_TIMEZONE,
    ):
        self._style = DefaultStreamStyle(fmt, defaults=defaults, coloured_keys=coloured_keys)
        if validate:
            self._style.validate()
        self.datefmt = datefmt
        self.tz = tz

    @property
    def _fmt(self) -> str:
        return self._style._fmt
    
    @_fmt.setter
    def _fmt(self, fmt: str) -> None:
        self._style._fmt = fmt
    
    def format(self, record: logging.LogRecord) -> str:
        '''
        Replace the funcName in the record with the fully qualified name.
        '''
        if (frame := inspect.currentframe()) is not None:
            i = 0
            while (frame := frame.f_back) is not None:  # traverse the stack to find the caller
                if i > 10:
                    raise RecursionError('Too many frames')
                if frame.f_globals.get('__name__') != 'logging':
                    record.funcName = frame.f_code.co_qualname
                    break
                i += 1
        return super().format(record)
    
    
class DefaultFileFormatter(DateFormatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            'asctime': self.formatTime(record=record),
            'levelname': record.levelname,
            'name': record.name,
            'module': record.module,
            'funcName': record.funcName,
            'lineno': record.lineno,
            'message': record.getMessage(),
        }
        return json.dumps(data)

def create_timed_rotating_file_handler(
    log_dir: Path, 
    log_name: str,
    formatter: Optional[logging.Formatter] = None,
    when: str = DEFAULT_LOG_FILE_INTERVAL,
    backup_count: int = DEFAULT_LOG_FILE_RETENTION,
    at_time: Optional[datetime.time] = DEFAULT_LOG_FILE_ROLL_TIME,
    **kwargs
) -> logging.handlers.TimedRotatingFileHandler:
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f'{log_name}.log'

    handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_file, 
        when=when, 
        backupCount=backup_count, 
        atTime=at_time, 
        **kwargs
    )
    if formatter is None:
        formatter = DefaultFileFormatter()
        handler.setFormatter(formatter)
    return handler

def add_timed_rotating_file_handler(
    logger: logging.Logger,
    log_dir: Path,
    formatter: Optional[logging.Formatter] = None,
    when: str = DEFAULT_LOG_FILE_INTERVAL,
    backup_count: int = DEFAULT_LOG_FILE_RETENTION,
    at_time: Optional[datetime.time] = DEFAULT_LOG_FILE_ROLL_TIME,
    **kwargs
) -> logging.handlers.TimedRotatingFileHandler:
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.TimedRotatingFileHandler):
            logger.warning(f'Ignoring. {logger.name} already has a rotating file handler ({handler.baseFilename}). {handler}')
            return handler
    handler = create_timed_rotating_file_handler(
        log_dir=log_dir, 
        log_name=logger.name, 
        formatter=formatter,
        when=when, 
        backup_count=backup_count, 
        at_time=at_time, 
        **kwargs
    )
    logger.addHandler(handler)
    return handler

def configure_logging(
    fmt: str = DEFAULT_LOG_FMT,
    datefmt: Optional[str] = None,
    validate: bool = True,
    coloured_keys: Optional[set[str]] = DEFAULT_COLOURED_FORE_KEYS,
    defaults: Optional[dict] = None,
    level=DEFAULT_LOG_LEVEL, 
    force: bool = False,
    capture_warnings: bool = True
):
    stream_handler = logging.StreamHandler()
    stream_formatter = DefaultStreamFormatter(
        fmt=fmt,
        datefmt=datefmt,
        validate=validate,
        coloured_keys=coloured_keys,
        defaults=defaults,
    )
    stream_handler.setFormatter(fmt=stream_formatter)

    handlers = [stream_handler]
    
    logging.basicConfig(handlers=handlers, level=level, force=force)
    logging.captureWarnings(capture_warnings)


@contextmanager
def temporary_logging_level(
    level: int, 
    loggers: Optional[Iterable[logging.Logger | str]] = None,
    exclude: Optional[Iterable[logging.Logger | str]] = None,
    suppress: Optional[Iterable[logging.Logger | str]] = None,
) -> Generator[None, None, None]:
    """
    Set the logging level for the specified loggers to the specified level.
    The loggers are set to the specified level, and the excluded loggers are set to their effective level.
    The suppressed loggers are disabled.
    Args:
        level (int): The logging level to set for the specified loggers.
        loggers (Iterable[logging.Logger | str]): The loggers to set to the specified level.
        exclude (Iterable[logging.Logger | str]): The loggers to exclude from the specified level.
        suppress (Iterable[logging.Logger | str]): The loggers to suppress.
    """
    def loggers_set(loggers: Optional[Iterable[logging.Logger | str]]) -> set[logging.Logger]:
        if loggers is None:
            return set()
        if isinstance(loggers, Iterable) and not isinstance(loggers, str):
            return {logging.getLogger(l) if isinstance(l, str) else l for l in loggers}
        raise TypeError(f'loggers must be an iterable of {logging.Logger} or {str}, not {type(loggers)}')

    if loggers is None:
        temp_loggers = {logging.getLogger()}
    else:
        temp_loggers = loggers_set(loggers=loggers)
    
    exclude_loggers = loggers_set(loggers=exclude)
    suppress_loggers = loggers_set(loggers=suppress)

    all_loggers = temp_loggers | exclude_loggers | suppress_loggers
    
    old_levels = {l: l.level for l in all_loggers}
    old_suppress = {l: l.disabled for l in suppress_loggers}
    
    # first get the effective level of the excluded loggers
    for l in exclude_loggers:
        l.setLevel(l.getEffectiveLevel())

    # then set the level of the loggers to the specified level
    for l in temp_loggers:
        if l not in exclude_loggers:
            l.setLevel(level)
    
    # then suppress the specified loggers
    for l in suppress_loggers:
        l.disabled = True

    try:
        yield
    finally:
        # return the system to the original state
        # reset all logger levels (includes the excluded loggers that may have previously inherited the level from their parent)
        for l, level in old_levels.items():
            l.setLevel(level)
        # reset the suppressed loggers to their original state
        for l, disabled in old_suppress.items():
            l.disabled = disabled
