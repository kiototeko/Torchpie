from injector import Module, provider, singleton
from ..environment import Args
import pyhocon
import logging


class ConfigModule(Module):

    @singleton
    @provider
    def provide_config(self, args: Args, logger: logging.Logger) -> pyhocon.ConfigTree:
        if args.config is None:
            logger.warning('Config not found.')
            return None

        config = pyhocon.ConfigFactory.parse_file(args.config)

        return config
