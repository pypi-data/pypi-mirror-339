# This file serves all MaleoAccess's Transfers

from __future__ import annotations
from .general import MaleoAccessGeneralTransfers
from .parameters import MaleoAccessParameters
from .results import MaleoAccessResults

class MaleoAccessTransfers:
    General = MaleoAccessGeneralTransfers
    Parameters = MaleoAccessParameters
    Results = MaleoAccessResults

__all__ = [
    "MaleoAccessTransfers",
    "MaleoAccessGeneralTransfers",
    "MaleoAccessParameters",
    "MaleoAccessResults"
]