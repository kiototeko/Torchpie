import argparse
from injector import provider, Module, singleton
from typing import Optional
import os
from torchpie.utils import get_timestamp


# def get_experiment_path(args: Args) -> Optional[str]:

#     timestamp = get_timestamp()
#     if args.experiment_path is None:
#         if args.debug:
#             experiment_path = os.path.join(
#                 'output', '{}_debug'.format(timestamp))
#         else:
#             experiment_path = os.path.join('output', timestamp)
#     else:
#         # No experiment path
#         if args.experiment_path == '!default':
#             return None
#         else:
#             experiment_path = args.experiment_path

#     # Make sure path is only made once
#     if args.local_rank == 0:
#         os.makedirs(experiment_path)
#     return experiment_path


class Args:
    _parser: argparse.ArgumentParser
    _args: argparse.Namespace

    def __init__(self):
        parser = argparse.ArgumentParser()
        self.experiment_path: Optional[str] = parser.add_argument(
            '-e',
            '--experiment-path',
            type=str,
            nargs='?',
            default='!default',
            required=False,
            help='path to save your experiment'
        )

        self.config: Optional[str] = parser.add_argument(
            '-c',
            '--config',
            type=str,
            nargs='?',
            required=False,
            help='path to config files'
        )

        self.debug: bool = parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='debug mode'
        )

        self.resume: str = parser.add_argument(
            '-r',
            '--resume',
            type=str,
            help='resume an experiment'
        )

        # This arg is for distributed
        self.local_rank: int = parser.add_argument(
            '--local_rank',
            default=0,
            type=int
        )

        self.parse_known_args(parser)
        self.create_experiment_path()

    def parse_args(self, parser: argparse.ArgumentParser):
        self._parser = parser
        self._args = self._parser.parse_args()
        self._assign_args()

    def parse_known_args(self, parser: argparse.ArgumentParser):
        self._parser = parser
        self._args, _ = self._parser.parse_known_args()
        self._assign_args()

    def _assign_args(self):

        for key, value in self.__dict__.items():
            if isinstance(value, argparse.Action):
                dest = value.dest
                self.__dict__[key] = self._args.__dict__[dest]

    def __contains__(self, key):
        '''
        Copy from argparse.Namespace
        '''
        return key in self.__dict__

    def create_experiment_path(self):
        timestamp = get_timestamp()
        if self.experiment_path is None:
            if self.debug:
                experiment_path = os.path.join(
                    'output', '{}_debug'.format(timestamp))
            else:
                experiment_path = os.path.join('output', timestamp)

        else:
            # No experiment path
            if self.experiment_path == '!default':
                experiment_path = None
            else:
                experiment_path = self.experiment_path

        if experiment_path is not None and self.local_rank == 0:
            os.makedirs(experiment_path, exist_ok=True)

        self.experiment_path = experiment_path


class ArgsModule(Module):
    '''
    For injection
    '''

    @singleton
    @provider
    def provide_args(self) -> Args:
        args = Args()
        return args
