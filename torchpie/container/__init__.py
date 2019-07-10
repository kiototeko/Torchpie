from injector import Injector
# from torchpie.argument.base import configure_args
from ..core.environment import ArgsModule
from ..core.config import ConfigModule
from ..core.logging import LoggerModule

# 在这里注册
modules = [
    ArgsModule(),
    ConfigModule(),
    LoggerModule(),
]

container = Injector(modules=modules)
