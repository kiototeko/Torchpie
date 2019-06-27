from injector import Injector
from torchpie.argument.base import configure_args

# 在这里注册
modules = [
    configure_args
]

container = Injector(modules=modules)
