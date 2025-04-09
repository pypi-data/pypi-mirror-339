# This file serves all MaleoSecurity's Results

from __future__ import annotations
from .general import MaleoSecurityGeneralResults

class MaleoSecurityResults:
    General = MaleoSecurityGeneralResults

__all__ = [
    "MaleoSecurityResults",
    "MaleoSecurityGeneralResults"
]