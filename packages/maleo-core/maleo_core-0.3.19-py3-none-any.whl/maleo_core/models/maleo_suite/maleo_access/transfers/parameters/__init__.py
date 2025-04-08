# This file serves all MaleoAccess's Parameters

from __future__ import annotations
from .general import MaleoAcccesGeneralParameters
from .service import MaleoAccessServiceParameters
from .client import MaleoAccessClientParameters

class MaleoAccessParameters:
    General = MaleoAcccesGeneralParameters
    Service = MaleoAccessServiceParameters
    Client = MaleoAccessClientParameters

__all__ = [
    "MaleoAccessParameters",
    "MaleoAcccesGeneralParameters",
    "MaleoAccessServiceParameters",
    "MaleoAccessClientParameters"
]