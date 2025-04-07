# This file serves all MaleoShared's General Parameters

from __future__ import annotations
from .service import MaleoSharedServiceGeneralParameters

class MaleoSharedGeneralParameters:
    Service = MaleoSharedServiceGeneralParameters

__all__ = ["MaleoSharedGeneralParameters", "MaleoSharedServiceGeneralParameters"]