from .experiment import debug, distributed
from .utils import set_exception_hook

# Never enter debug mode when distributed.
# ipdb under distributed is buggy.
if debug and not distributed:
    set_exception_hook()
