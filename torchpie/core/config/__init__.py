from injector import Module, provider, singleton
from ..environment import Args
import pyhocon


class ConfigModule(Module):

    @singleton
    @provider
    def provide_config(self, args: Args) -> pyhocon.ConfigTree:
        if args.config is None:
            print('no config in args')
            return None
        
        config = pyhocon.ConfigFactory.parse_file(args.config)


        return config

        