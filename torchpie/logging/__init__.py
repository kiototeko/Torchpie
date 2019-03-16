import logging
import sys
import os
from torchpie.experiment import experiment_path, args
from injector import Module, singleton, provider


LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'


def get_logger(name: str, log_file: str):
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

    if args.debug:
        logger.setLevel(logging.DEBUG)

    return logger


# logger = get_logger('torchpie', 'result.log')


class Logger(logging.Logger):
    pass


class LoggerModule(Module):

    @singleton
    @provider
    def provide_logger(self) -> Logger:
        return get_logger('torchpie', 'result.log')
