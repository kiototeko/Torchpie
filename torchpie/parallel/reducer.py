import torch
import torch.distributed as dist
from torchpie.experiment import world_size


def reduce_tensor(tensor: torch.Tensor) -> torch.Tensor:
    '''
    loss = reduce_tensor(loss)
    acc1 = reduce_tensor(acc1)
    acc5 = reduce_tensor(acc5)
    '''
    rt = tensor.clone()
    dist.all_reduce(rt, op=dist.ReduceOp.SUM)
    rt /= world_size
    return rt
