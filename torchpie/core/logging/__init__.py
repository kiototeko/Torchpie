import logging
from injector import Module, singleton, provider
from torchpie.parallel import rank0_wrapper
from ..environment import Args

LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(filename)s:%(lineno)d %(message)s'

class LoggerModule(Module):

    
    def provide_logger(self, args: Args) -> logging.Logger:
        
        logger = None