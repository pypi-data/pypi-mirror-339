import warnings
import sim_lab

warnings.warn(
    "The 'simnexus' package is deprecated and will be removed in a future version. "
    "Please use 'sim-lab' instead. Install with 'pip install sim-lab' and "
    "update your imports from 'import simnexus' to 'import sim_lab'.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export sim_lab as simnexus for backward compatibility
from sim_lab import *

__version__ = "0.3.1"