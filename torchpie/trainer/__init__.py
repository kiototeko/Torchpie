from torch import nn, optim
from torch.optim.lr_scheduler import _LRScheduler
import torch
import shutil
from torchpie.experiment import experiment_path
from torchpie.logging import logger
from torchpie.config import config
from injector import inject
import os


class Trainer:
    model: nn.Module = None
    criterion: nn.Module = None
    optimizer: optim.Optimizer = None
    lr_scheduler: _LRScheduler = None
    data_parallel: nn.DataParallel = None
    is_data_parallel: bool = False
    epoch: int = 0
    epochs: int = 0

    @inject
    def __init__(self):
        self.logger = logger
        self.config = config

    def model_state_dict(self, destination=None, prefix='', keep_vars=False) -> dict:
        if self.is_data_parallel:
            return self.model.module.state_dict(destination, prefix, keep_vars)
        else:
            return self.model.state_dict(destination, prefix, keep_vars)

    def state_dict(self, destination=None, prefix='', keep_vars=False) -> dict:
        '''
        Can be rewrite, think about what to save
        '''
        state_dict = {
            'epoch': self.epoch,  # epoch 0 or epoch 1?
            'model_state_dict': self.model_state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict()
        }

        return state_dict

    def save_checkpoint(self, is_best=False, filename='checkpoint.pth.tar'):
        checkpoint_path = os.path.join(experiment_path, filename)
        torch.save(self.state_dict(), checkpoint_path)

        # We don't know what is best
        if is_best:
            best_model_path = os.path.join(
                experiment_path, 'best_model.pth.tar')
            shutil.copyfile(checkpoint_path, best_model_path)

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    def step(self):
        self.epoch += 1
