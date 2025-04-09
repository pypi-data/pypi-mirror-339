# This file serves all MaleoShared's Cient Parameters

from __future__ import annotations
from .service import MaleoSharedServiceClientParameters

class MaleoSharedClientParameters:
    Service = MaleoSharedServiceClientParameters

__all__ = ["MaleoSharedClientParameters", "MaleoSharedServiceClientParameters"]