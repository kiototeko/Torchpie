import argparse
from injector import provider, Module, singleton
from typing import Optional


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


class ArgsModule(Module):
    '''
    For injection
    '''

    @singleton
    @provider
    def provide_args(self) -> Args:
        args = Args()
        return args
