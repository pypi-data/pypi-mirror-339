# This file serves all MaleoShared's Transfers

from __future__ import annotations
from .parameters import MaleoSharedParameters
from .results import MaleoSharedResults

class MaleoSharedTransfers:
    Parameters = MaleoSharedParameters
    Results = MaleoSharedResults

__all__ = ["MaleoSharedTransfers", "MaleoSharedParameters", "MaleoSharedResults"]