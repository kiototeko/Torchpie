import os
import torch
import shutil
# from torchpie.logging import rank0
from torchpie.parallel import rank0_fn

@rank0_fn
def save_checkpoint(state: dict, is_best=False, folder='', filename='checkpoint.pth.tar'):
    filename = os.path.join(folder, filename)
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, os.path.join(folder, 'model_best.pth.tar'))
