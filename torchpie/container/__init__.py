from injector import Injector
from torchpie.argument.base import Args

# 在这里注册
modules = [
    Args
]

container = Injector(modules=modules)
