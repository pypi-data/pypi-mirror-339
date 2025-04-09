# This file serves all MaleoSecurity's Schemas

from __future__ import annotations
from .responses import MaleoSecurityResponsesSchemas

class MaleoSecuritySchemas:
    Responses = MaleoSecurityResponsesSchemas

__all__ = ["MaleoSecuritySchemas", "MaleoSecurityResponsesSchemas"]