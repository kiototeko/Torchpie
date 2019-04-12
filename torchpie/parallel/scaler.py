from torchpie.experiment import world_size


def scale_lr(lr: float, batch_size: int) -> float:
    '''
    https://github.com/NVIDIA/apex/blob/master/examples/imagenet/main_amp.py#L144
    :param lr: learning rate
    :param batch_size: batch size
    :param world_size: world size, num gpus
    :return:
    '''
    return lr * float(batch_size * world_size) / 256.0
