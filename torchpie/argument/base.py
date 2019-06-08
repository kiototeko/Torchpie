import argparse
from .functional import get_experiment_path
from typing import Optional

from injector import Binder, singleton, Key, inject, Module

ExperimentPath = Key('experiment-path')


class Argument:
    def __init__(self, args: argparse.Namespace):
        self.debug: bool = args.debug
        self.config: Optional[str] = args.config
        self.experiment: Optional[str] = args.experiment
        self.local_rank: int = args.local_rank
        self.resume: Optional[str] = args.resume

    def __contains__(self, key):
        return key in self.__dict__


def configure_args(binder: Binder):
    '''创建args对象，并注入container'''

    parser = argparse.ArgumentParser('TorchPie')
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
    binder.bind(argparse.Namespace, to=args, scope=singleton)

    argument = Argument(args)
    binder.bind(Argument, to=argument, scope=singleton)

    experiment_path = get_experiment_path(argument)
    binder.bind(ExperimentPath, to=experiment_path, scope=singleton)
