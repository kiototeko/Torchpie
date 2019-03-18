import logging
import sys
import os
from torchpie.experiment import experiment_path, debug, rank0


LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'


@rank0
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

    return logger


class Logger(logging.Logger):

    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)

    def setLevel(self, level: int):
        super(Logger, self).setLevel(level)

    def debug(self, msg, *args, **kwargs):
        self.inner.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.inner.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.inner.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.inner.error(msg, *args, **kwargs)


logger = Logger()
