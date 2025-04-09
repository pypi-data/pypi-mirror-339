# This file serves all MaleoSecurity's General Parameters

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralParameters

class MaleoSecurityGeneralParameters:
    Key = MaleoSecurityKeyGeneralParameters

__all__ = [
    "MaleoSecurityGeneralParameters",
    "MaleoSecurityKeyGeneralParameters"
]