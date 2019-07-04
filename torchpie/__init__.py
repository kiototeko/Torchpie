# from .utils import set_exception_hook
# from .argument import args
# from .argument.functional import is_distributed

# from typing import Optional

__version__ = '0.2.0'

# 这些变量直接用tp.[name]访问，挂在tp上以免污染全局变量。
# local_rank: int = args.local_rank
# debug: bool = args.debug
# experiment_path: Optional[str] = experiment_path

# distributed: bool = is_distributed()

# Never enter debug mode when distributed.
# ipdb under distributed is buggy.
# if debug and not distributed:
#     set_exception_hook()
