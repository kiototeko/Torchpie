'''

'''

import argparse
import time
import os
from typing import Optional
import torch

parser = argparse.ArgumentParser('experiment')
parser.add_argument('-e', '--experiment', type=str, nargs='?', default='!default', required=False,
                    help='experiment path')

# 要么就不指定，指定了就一定要填名称
# parser.add_argument('-e', '--experiment', type=str, required=False,
#                     help='experiment path')
parser.add_argument('-c', '--config', type=str, nargs='?',
                    required=False, help='path to config files')
parser.add_argument('-d', '--debug', action='store_true', help='debug mode')

parser.add_argument('-r', '--resume', type=str, help='resume model')

# For DistributedDataParallel, default must be 0
parser.add_argument('--local_rank', default=0, type=int)

args, _ = parser.parse_known_args()


def get_experiment_path(experiment: str, debug: bool, local_rank=0, resume=None) -> Optional[str]:

    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    if experiment is None:
        if debug:
            experiment_path = os.path.join(
                'output', '{}_debug'.format(timestamp))
        else:
            experiment_path = os.path.join('output', timestamp)
    else:
        # No experiment path
        if experiment == '!default':
            return None
        else:
            experiment_path = experiment

    # Make sure path is only made once
    if local_rank == 0 and resume is None:
        os.makedirs(experiment_path)
    return experiment_path


def is_distributed():
    if 'WORLD_SIZE' in os.environ:
        return int(os.environ['WORLD_SIZE']) > 1
    else:
        return False


experiment_path = get_experiment_path(
    args.experiment, args.debug, local_rank=args.local_rank, resume=args.resume)
debug: bool = args.debug
local_rank: int = args.local_rank
distributed: bool = is_distributed()
resume: str = args.resume
world_size: int = int(
    os.environ['WORLD_SIZE']) if distributed else 1

if distributed:
    torch.cuda.set_device(local_rank)
    torch.distributed.init_process_group(backend='nccl',
                                         init_method='env://')
