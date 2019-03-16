import argparse
import time
import os

parser = argparse.ArgumentParser('experiment')
# parser.add_argument('-e', '--experiment', type=str, nargs='?', default='!default', required=False,
#                     help='experiment path')

# 要么就不指定，指定了就一定要填名称
parser.add_argument('-e', '--experiment', type=str, required=False,
                    help='experiment path')
parser.add_argument('-c', '--config', type=str, nargs='?',
                    required=False, help='path to config files')
parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
args, _ = parser.parse_known_args()


def get_experiment_path(experiment: str, debug: bool) -> str:

    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    if experiment is None:
        if debug:
            experiment_path = os.path.join(
                'output', '{}_debug'.format(timestamp))
        else:
            experiment_path = os.path.join('output', timestamp)
    else:
        experiment_path = experiment

    os.makedirs(experiment_path, exist_ok=True)
    return experiment_path


experiment_path = get_experiment_path(args.experiment, args.debug)
debug: bool = args.debug
