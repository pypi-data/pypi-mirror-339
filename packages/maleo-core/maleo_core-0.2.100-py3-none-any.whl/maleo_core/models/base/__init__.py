# This file serves collections of Base Models

from __future__ import annotations
from .general import BaseGeneralModels
from .schemas import BaseSchemas
from .transfers import BaseTransfers

class BaseModels:
    General = BaseGeneralModels
    Schemas = BaseSchemas
    Transfers = BaseTransfers

__all__ = ["BaseModels", "BaseSchemas", "BaseTransfers"]