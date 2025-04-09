# This file serves all MaleoShared's Parameters

from __future__ import annotations
from .general import MaleoSharedGeneralParameters
from .service import MaleoSharedServiceParameters
from .client import MaleoSharedClientParameters

class MaleoSharedParameters:
    General = MaleoSharedGeneralParameters
    Service = MaleoSharedServiceParameters
    Client = MaleoSharedClientParameters

__all__ = ["MaleoSharedParameters", "MaleoSharedGeneralParameters", "MaleoSharedServiceParameters", "MaleoSharedClientParameters"]