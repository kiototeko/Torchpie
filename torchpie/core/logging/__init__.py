import logging
from injector import Module, singleton, provider
from ..environment import Args
from torchpie.utils import get_timestamp
import sys
import os

LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'


class LoggerModule(Module):

    @singleton
    @provider
    def provide_logger(self, args: Args) -> logging.Logger:

        logger = logging.getLogger('torchpie')

        log_format = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'
        formatter = logging.Formatter(log_format)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if args.experiment_path is not None:
            # Add timestamp to filename
            file_handler = logging.FileHandler(
                os.path.join(args.experiment_path, f'result_{get_timestamp()}.log'))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            logger.warning(
                'No experiment path, no log file will be generated.')

        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info('Logger for local_rank={}'.format(args.local_rank))

        return logger
