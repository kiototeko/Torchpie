import os



def is_distributed() -> bool:
    '''
    https://github.com/NVIDIA/apex/blob/master/examples/imagenet/main_amp.py#L112
    '''
    if 'WORLD_SIZE' in os.environ:
        return int(os.environ['WORLD_SIZE']) > 1
    else:
        return False


def do_nothing(*args, **kwargs):
    '''
    什么也不做
    '''
    pass
