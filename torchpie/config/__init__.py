import pyhocon
from torchpie.experiment import args, experiment_path, local_rank
import argparse
import os
from torchpie.snapshot import snapshot_as_zip
from torchpie.logging import logger, rank0


def compact_keys(config: pyhocon.ConfigTree):
    '''
    Flatten all keys on config
    :param config: pyhocon.ConfigTree
    :return: str
    '''
    key_stack = []

    def walk(tree: pyhocon.ConfigTree):
        for key, value in tree.items():
            # print("value={}, type={}".format(value, type(value)))
            key_stack.append(key)
            if isinstance(value, pyhocon.ConfigTree):
                if len(value) == 0:
                    key_str = '.'.join(key_stack)
                    yield key_str, value
                else:
                    yield from walk(value)
            else:
                key_str = '.'.join(key_stack)
                yield key_str, value
            key_stack.pop()

    yield from walk(config)


def get_config() -> pyhocon.ConfigTree:
    if args.config is None:
        logger.warning('no config')
        return None

    config = pyhocon.ConfigFactory.parse_file(args.config)

    config_parser = argparse.ArgumentParser('config')

    # set key on config parser
    for key, value in compact_keys(config):
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

    if experiment_path is not None and rank0():
        config_file = os.path.join(experiment_path, 'config.conf')
        with open(config_file, 'w') as f:
            f.write(pyhocon.HOCONConverter.to_hocon(config))

        logger.info('Config is saved to {}'.format(config_file))

        # save all code and config file
        snapshot_as_zip(
            os.path.join(experiment_path, 'code.zip'),
            file_list=[config_file] +
            config.get_list('snapshot.files', default=[]),
            patterns=['**/*.py'] + config.get_list('snapshot.patterns', default=[]))
    else:
        logger.warning('No experiment path, no config will be saved.')

    return config


config = get_config()
