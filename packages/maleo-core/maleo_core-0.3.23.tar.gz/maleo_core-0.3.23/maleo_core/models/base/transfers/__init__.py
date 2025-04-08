# This file serves collections of Base Transfers

from __future__ import annotations
from .parameters import BaseParameters
from .results import BaseResults

class BaseTransfers:
    Parameters = BaseParameters
    Results = BaseResults

    __all__ = ["BaseTransfers", "BaseParameters", "BaseResults"]