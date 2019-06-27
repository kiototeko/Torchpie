import time
from typing import Optional
import os


def get_experiment_path(args) -> Optional[str]:
    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())

    if args.experiment_path is None:
        if args.debug:
            experiment_path = os.path.join(
                'output', '{}_debug'.format(timestamp))
        else:
            experiment_path = os.path.join('output', timestamp)
    else:
        # No experiment path
        if args.experiment_path == '!default':
            return None
        else:
            experiment_path = args.experiment_path

    # Make sure path is only made once
    if args.local_rank == 0 and args.resume is None:
        os.makedirs(experiment_path)
    return experiment_path


def is_distributed() -> bool:
    if 'WORLD_SIZE' in os.environ:
        return int(os.environ['WORLD_SIZE']) > 1
    else:
        return False


# def set_cuda_visible_devices(args: Argument):
#     """
#     if args.gpu exists, set CUDA_VISIBLE_DEVICES
#     """
#     if args.gpu is not None:
#         os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
