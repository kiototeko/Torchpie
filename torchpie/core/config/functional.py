import pyhocon
from zipfile import ZipFile
from glob import glob
from typing import Optional, List


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


def take_snapshot_as_zip(name: str, file_list: Optional[List[str]] = None, patterns=['**/*.py']) -> List[str]:
    with ZipFile(name, 'w') as zf:

        if file_list is None:
            file_list = []

        for pattern in patterns:
            file_list.extend(glob(pattern, recursive=True))

        for filename in file_list:
            zf.write(filename)

    return file_list
