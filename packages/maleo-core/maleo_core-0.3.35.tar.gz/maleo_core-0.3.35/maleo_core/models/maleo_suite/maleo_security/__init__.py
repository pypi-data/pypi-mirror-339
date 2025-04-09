# This file serves all MaleoSecurity's models

from __future__ import annotations
from .schemas import MaleoSecuritySchemas
from .transfers import MaleoSecurityTransfers

class MaleoSecurityModels:
    Schemas = MaleoSecuritySchemas
    Transfers = MaleoSecurityTransfers

__all__ = ["MaleoSecurityModels", "MaleoSecuritySchemas", "MaleoSecurityTransfers"]