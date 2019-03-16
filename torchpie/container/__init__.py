from injector import Injector
from torchpie.config import ConfigModule
from torchpie.logging import LoggerModule


# Global injector
container = Injector([ConfigModule, LoggerModule])
