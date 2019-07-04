from injector import Injector
# from torchpie.argument.base import configure_args
from torchpie.core.environment import ArgsModule

# 在这里注册
modules = [
    ArgsModule
]

container = Injector(modules=modules)
