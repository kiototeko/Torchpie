# from .functional import is_distributed, do_nothing
from . import functional as F
from ..environment import args
import torch
import inspect
from functools import wraps


distributed: bool = F.is_distributed()
local_rank: int = args.local_rank
local_rank_is_0: bool = local_rank == 0

# https://github.com/NVIDIA/apex/blob/master/examples/imagenet/main_amp.py#L118
world_size: int = 1

if distributed:
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend='nccl',
                                         init_method='env://')
    world_size = torch.distributed.get_world_size()


class FakeObj:

    def __getattr__(self, name):
        return do_nothing


def do_nothing(*args, **kwargs) -> FakeObj:
    '''
    什么也不做
    '''
    return FakeObj()


def rank0_fn(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if local_rank_is_0 or kwargs.get('run_anyway', False):
            kwargs.pop('run_anyway', None)
            return fn(*args, **kwargs)
        else:
            return FakeObj()

    return wrapper


def rank0_cls(cls):

    for key, value in cls.__dict__.items():
        if callable(value):
            setattr(cls, key, rank0_fn(value))

    return cls


def rank0_obj(obj):
    '''
    Too tricky, I don't like it.
    '''
    cls = obj.__class__
    for key, value in cls.__dict__.items():
        if callable(value):
            obj.__dict__[key] = rank0_fn(value).__get__(obj, cls)

    return obj


def rank0(something):
    '''
    Something may be function, class or object, wrap it anyway.
    '''
    if inspect.isfunction(something):
        return rank0_fn(something)
    elif inspect.isclass(something):
        return rank0_cls(something)
    else:
        return rank0_obj(something)
