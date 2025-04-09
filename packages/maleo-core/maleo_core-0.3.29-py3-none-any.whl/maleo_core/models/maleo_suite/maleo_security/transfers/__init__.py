# This file serves all MaleoSecurity's Transfers

from __future__ import annotations
from .general import MaleoSecurityGeneralTransfers

class MaleoSecurityTransfers:
    General = MaleoSecurityGeneralTransfers

__all__ = [
    "MaleoSecurityTransfers",
    "MaleoSecurityGeneralTransfers"
]