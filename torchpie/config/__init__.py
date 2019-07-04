from ..container import container
import pyhocon
from typing import Optional

config: Optional[pyhocon.ConfigTree] = container.get(pyhocon.ConfigTree)
