# This file serves all MaleoSecurity's Parameters

from __future__ import annotations
from .general import MaleoSecurityGeneralParameters

class MaleoSecurityParameters:
    General = MaleoSecurityGeneralParameters

__all__ = [
    "MaleoSecurityParameters",
    "MaleoSecurityGeneralParameters"
]