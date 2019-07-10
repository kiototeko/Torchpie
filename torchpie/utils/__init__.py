import sys
from .exception_hook import ExceptionHook
import time


def set_exception_hook():
    sys.excepthook = ExceptionHook()


def get_timestamp(fmt: str = '%Y%m%d_%H%M%S') -> str:
    timestamp = time.strftime(fmt, time.localtime())
    return timestamp
