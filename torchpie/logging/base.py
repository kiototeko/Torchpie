import logging
import sys
import os
from torchpie.experiment import experiment_path, debug, local_rank
import typing

LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'


def do_nothing(*args, **kwargs):
    pass


def rank0(func=None):
    if func is None:
        return local_rank == 0

    def wrapper(*args, **kwargs):
        if False or local_rank == 0:
            return func(*args, **kwargs)
        else:
            return do_nothing
        # return do_nothing

    return wrapper


# @rank0
def get_logging_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if experiment_path is not None:
        file_handler = logging.FileHandler(
            os.path.join(experiment_path, log_file))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger.warning('No experiment path, no log file will be generated.')

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.info('Logger for local_rank={}'.format(local_rank))

    return logger


# Fake type, do not call super().__init__()
class Logger:

    def __init__(self):
        self.inner = get_logging_logger('torchpie', 'result.log')

    @rank0
    def __getattr__(self, name):
        # print(f'call logger {name}')
        # return do_nothing
        return getattr(self.inner, name)
