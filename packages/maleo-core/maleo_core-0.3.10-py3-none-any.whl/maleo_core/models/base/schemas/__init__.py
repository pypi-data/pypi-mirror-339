# This file serves all Base Schemas

from __future__ import annotations
from .responses import BaseResponsesSchemas

class BaseSchemas:
    Responses = BaseResponsesSchemas

__all__ = ["BaseSchemas", "BaseResponsesSchemas"]