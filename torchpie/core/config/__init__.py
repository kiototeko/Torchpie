from injector import Module, provider, singleton
from ..environment import Args
import pyhocon
import logging
import argparse
from . import functional as F
import os


class ConfigModule(Module):

    @singleton
    @provider
    def provide_config(self, args: Args, logger: logging.Logger) -> pyhocon.ConfigTree:
        if args.config is None:
            logger.warning('Config not found.')
            return None

        config = pyhocon.ConfigFactory.parse_file(args.config)

        config_parser = argparse.ArgumentParser('config')

        # set key on config parser
        for key, value in F.compact_keys(config):
            config_parser.add_argument(f'--c.{key}', type=type(value))

        config_args, unknown_args = config_parser.parse_known_args()

        # 检查是否有输错key
        for arg in unknown_args:
            # remove -- from --c.xxx
            if arg[2:].startswith('c.'):
                raise Exception('wrong key: {}'.format(arg))

        # Replace config
        for key, value in config_args.__dict__.items():
            if value is not None:
                logger.info(f'Replace: {key} => {value}')
                # You can't directly set this OrderedDict, use put instead
                # The value type can only be str, it works but is ugly
                # I don't know how to get item type from pyhocon.ConfigTree
                # Take c.[this part] from key
                config.put(key[2:], value)

        if args.experiment_path is not None and args.local_rank == 0:
            config_file = os.path.join(args.experiment_path, 'config.conf')
            with open(config_file, 'w') as f:
                f.write(pyhocon.HOCONConverter.to_hocon(config))

            logger.info('Config is saved to {}'.format(config_file))

            # save all code and config file
            file_list = F.take_snapshot_as_zip(
                os.path.join(args.experiment_path, 'code.zip'),
                file_list=[config_file] +
                config.get_list('snapshot.files', default=[]),
                patterns=['**/*.py'] +
                config.get_list('snapshot.patterns', default=[])
            )

            logger.info('taking a snapshot of \n{}'.format(file_list))
        else:
            logger.warning('No experiment path, no config will be saved.')

        return config
