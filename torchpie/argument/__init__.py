from torchpie.container import container
from .base import ExperimentPath, Argument
from typing import Optional
from .functional import is_distributed

args: Argument = container.get(Argument)
experiment_path: Optional[str] = container.get(ExperimentPath)


