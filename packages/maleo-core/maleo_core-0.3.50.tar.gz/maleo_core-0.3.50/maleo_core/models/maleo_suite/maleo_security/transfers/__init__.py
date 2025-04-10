# This file serves all MaleoSecurity's Transfers

from __future__ import annotations
from .general import MaleoSecurityGeneralTransfers
from .parameters import MaleoSecurityParameters
from .results import MaleoSecurityResults

class MaleoSecurityTransfers:
    General = MaleoSecurityGeneralTransfers
    Parameters = MaleoSecurityParameters
    Results = MaleoSecurityResults

__all__ = [
    "MaleoSecurityTransfers",
    "MaleoSecurityGeneralTransfers",
    "MaleoSecurityParameters",
    "MaleoSecurityResults"
]