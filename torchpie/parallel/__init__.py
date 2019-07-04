from .functional import is_distributed
from ..environment import args
import torch

distributed: bool = is_distributed()
local_rank: int = args.local_rank

# https://github.com/NVIDIA/apex/blob/master/examples/imagenet/main_amp.py#L118
world_size: int = 1

if distributed:
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend='nccl',
                                         init_method='env://')
    world_size = torch.distributed.get_world_size()
