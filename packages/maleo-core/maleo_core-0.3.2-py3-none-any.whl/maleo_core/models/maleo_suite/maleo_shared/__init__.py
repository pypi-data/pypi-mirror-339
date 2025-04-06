# This file serves all MaleoShared's models

from __future__ import annotations
from .schemas import MaleoSharedSchemas
from .transfers import MaleoSharedTransfers

class MaleoSharedModels:
    Schemas = MaleoSharedSchemas
    Transfers = MaleoSharedTransfers

__all__ = ["MaleoSharedModels", "MaleoSharedSchemas", "MaleoSharedTransfers"]