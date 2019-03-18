'''

'''

import argparse
import time
import os
from typing import Optional

parser = argparse.ArgumentParser('experiment')
parser.add_argument('-e', '--experiment', type=str, nargs='?', default='!default', required=False,
                    help='experiment path')

# 要么就不指定，指定了就一定要填名称
# parser.add_argument('-e', '--experiment', type=str, required=False,
#                     help='experiment path')
parser.add_argument('-c', '--config', type=str, nargs='?',
                    required=False, help='path to config files')
parser.add_argument('-d', '--debug', action='store_true', help='debug mode')

# For DistributedDataParallel, default must be 0
parser.add_argument('--local_rank', default=0, type=int)

args, _ = parser.parse_known_args()


def get_experiment_path(experiment: str, debug: bool) -> Optional[str]:

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

    os.makedirs(experiment_path, exist_ok=True)
    return experiment_path


def is_distributed():
    if 'WORLD_SIZE' in os.environ:
        return int(os.environ['WORLD_SIZE']) > 1
    else:
        return False


def rank0(func):
    def wrapper(*args, **kwargs):
        if args.local_rank == 0:
            return func(*args, **kwargs)


experiment_path = get_experiment_path(args.experiment, args.debug)
debug: bool = args.debug
local_rank: int = args.local_rank
distributed: bool = is_distributed()
