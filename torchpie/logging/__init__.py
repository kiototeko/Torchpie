from ..container import container
from ..parallel import rank0_wrapper
import logging


logger: logging.Logger = rank0_wrapper(container.get(logging.Logger))
