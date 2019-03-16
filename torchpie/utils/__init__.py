import sys
from .exception_hook import ExceptionHook
from torchpie.container import container
from torchpie.config import Config
from torchpie.logging import Logger


def set_exception_hook():
    sys.excepthook = container.get(ExceptionHook)


def config() -> Config:
    '''
    helper function to get config
    '''
    return container.get(Config)


def logger() -> Logger:
    '''
    helper function to get logger
    '''
    return container.get(Logger)
