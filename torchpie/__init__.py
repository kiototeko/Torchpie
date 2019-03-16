from .experiment import debug
from .utils import set_exception_hook

if debug:
    set_exception_hook()
