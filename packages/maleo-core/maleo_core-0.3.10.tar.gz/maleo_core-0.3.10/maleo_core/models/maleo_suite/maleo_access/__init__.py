# This file serves all MaleoAccess's models

from __future__ import annotations
from .schemas import MaleoAccessSchemas
from .transfers import MaleoAccessTransfers

class MaleoAccessModels:
    Schemas = MaleoAccessSchemas
    Transfers = MaleoAccessTransfers

__all__ = ["MaleoAccessModels", "MaleoAccessSchemas", "MaleoAccessTransfers"]