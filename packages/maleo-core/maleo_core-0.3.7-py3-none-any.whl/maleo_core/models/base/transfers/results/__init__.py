# This file serves all Base Results

from __future__ import annotations
from .clients import BaseClientResults
from .services import BaseServiceResults

class BaseResults:
    Client = BaseClientResults
    Service = BaseServiceResults

__all__ = ["BaseResults", "BaseClientResults", "BaseServiceResults"]