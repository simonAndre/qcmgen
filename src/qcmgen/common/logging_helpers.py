import logging
from enum import Enum, IntEnum
from functools import partial, wraps
from time import time
from typing import Optional


def scopelogging(func):
    "debug log for enter and exit of the func"

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger: Optional[logging.Logger] = None
        t: float = 0
        if hasattr(self, "logger"):
            logger = self.logger
        if logger:
            logger.debug(f"enter {func.__name__}")
            t = time()

        res = func(self, *args, **kwargs)

        if logger:
            elapsed = (time() - t) * 1000
            logger.debug(f"exit {func.__name__}, execution time : {elapsed}ms")
        return res

    return wrapper


class CustLogger(Enum):
    StdOut = "output-stdout"
    """to print a text out to the stdout without specific formatting to be
    able to redirect it to a file or other. Uses the output-stdout logger"""


class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


_prom_counter_logger_hits = None



def output_stdout(msg: str):
    _logger = get_logger(logger_name=CustLogger.StdOut.value)
    _logger.info(msg)


def _logoverwrite(
    superfunc,
    logger_name,
    level: int,
    msg: object,
    args,
    exc_info=None,
    extra=None,
    stack_info: bool = False,
    stacklevel: int = 1,
):
    superfunc(level, msg, args, exc_info, extra, stack_info, stacklevel)


def logger_factory(
    logger_name: str,
) -> logging.Logger:
    _logger = logging.getLogger(logger_name)
    _logger._log = partial(_logoverwrite, _logger._log, logger_name)
    return _logger


_loggers = {}


def get_logger(logger_name) -> logging.Logger:
    global _loggers
    if logger_name in _loggers:
        return _loggers[logger_name]
    else:
        _loggers[logger_name] = logger_factory(logger_name)
        return _loggers[logger_name]
