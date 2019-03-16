import sys
from .exception_hook import ExceptionHook


def set_exception_hook():
    sys.excepthook = ExceptionHook()
