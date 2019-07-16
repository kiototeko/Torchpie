from ..container import container
from ..parallel import rank0_obj
import logging


logger: logging.Logger = rank0_obj(container.get(logging.Logger))
