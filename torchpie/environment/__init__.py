from ..container import container
from ..core.environment import Args


args: Args = container.get(Args)

experiment_path: str = args.experiment_path
