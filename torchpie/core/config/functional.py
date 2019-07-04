import pyhocon

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
