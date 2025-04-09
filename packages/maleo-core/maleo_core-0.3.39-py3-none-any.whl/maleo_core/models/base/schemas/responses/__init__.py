# This file serves all Base Responses Schemas

from __future__ import annotations
from .general import BaseGeneralResponsesSchemas
from .service import BaseServiceResponsesSchemas

class BaseResponsesSchemas:
    General = BaseGeneralResponsesSchemas
    Service = BaseServiceResponsesSchemas

__all__ = ["BaseResponsesSchemas", "BaseGeneralResponsesSchemas", "BaseServiceResponsesSchemas"]