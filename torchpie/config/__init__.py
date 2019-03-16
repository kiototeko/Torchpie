import pyhocon
from torchpie.experiment import args, experiment_path
import argparse
import os
from torchpie.snapshot import snapshot_as_zip
from torchpie.logging import logger


def compact_keys(config: pyhocon.ConfigTree):
    '''
    Flatten all keys on config
    :param config: pyhocon.ConfigTree
    :return: str
    '''
    key_stack = []

    def walk(tree: pyhocon.ConfigTree):
        for key, value in tree.items():
            key_stack.append(key)
            if isinstance(value, pyhocon.ConfigTree):
                if len(value) == 0:
                    key_str = '.'.join(key_stack)
                    yield key_str
                else:
                    yield from walk(value)
            else:
                key_str = '.'.join(key_stack)
                yield key_str
            key_stack.pop()

    yield from walk(config)


def get_config() -> pyhocon.ConfigTree:
    if args.config is None:
        logger.warning('no config')
        return None

    config = pyhocon.ConfigFactory.parse_file(args.config)

    config_parser = argparse.ArgumentParser('config')

    # set key on config parser
    for key in compact_keys(config):
        config_parser.add_argument(f'--{key}')

    config_args, _ = config_parser.parse_known_args()

    # Replace config
    for key, value in config_args.__dict__.items():
        if value is not None:
            logger.info(f'Replace: {key} => {value}')
            # You can't directly set this OrderedDict, use put instead
            # The value type can only be str, it works but is ugly
            # I don't know how to get item type from pyhocon.ConfigTree
            config.put(key, value)

    if experiment_path is not None:
        config_file = os.path.join(experiment_path, 'config.conf')
        with open(config_file, 'w') as f:
            f.write(pyhocon.HOCONConverter.to_hocon(config))

        logger.info('config is saved to {}'.format(config_file))

        # save all code and config file
        snapshot_as_zip(os.path.join(
            experiment_path, 'code.zip'), [config_file])

    return config


config = get_config()
