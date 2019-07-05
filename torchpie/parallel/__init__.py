from .functional import is_distributed, do_nothing
from ..environment import args
import torch
import inspect
from functools import wraps


distributed: bool = is_distributed()
local_rank: int = args.local_rank
local_rank_is_0: bool = local_rank == 0

# https://github.com/NVIDIA/apex/blob/master/examples/imagenet/main_amp.py#L118
world_size: int = 1

if distributed:
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend='nccl',
                                         init_method='env://')
    world_size = torch.distributed.get_world_size()


# def rank0(something):
#     if inspect.isclass(something):
#         def rank0_getattribute(self, name):
#             if local_rank_is_0:
#                 return super(something, self).__getattribute__(name)
#             else:
#                 return do_nothing

#         something.__getattribute__ = rank0_getattribute
#         return something
#     if inspect.isfunction(something):
#         if local_rank_is_0:
#             return something
#         else:
#             return do_nothing



def do_nothing(*args, **kwargs):
    '''
    什么也不做
    '''
    pass


def rank0_fn(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if local_rank_is_0 or kwargs.get('run_anyway', False):
            kwargs.pop('run_anyway', None)
            return fn(*args, **kwargs)
        else:
            return do_nothing

    return wrapper


def rank0_cls(cls):

    for key, value in cls.__dict__.items():
        if callable(value):
            setattr(cls, key, rank0_fn(value))

    return cls


def rank0_wrapper(obj, cls):

    for key, value in cls.__dict__.items():

        if callable(value):

            obj.__dict__[key] = rank0_fn(value).__get__(obj, cls)

    return obj