# This file serves all MaleoAccess's Schemas

from __future__ import annotations
from .responses import MaleoAccessResponsesSchemas

class MaleoAccessSchemas:
    Responses = MaleoAccessResponsesSchemas

__all__ = ["MaleoAccessSchemas", "MaleoAccessResponsesSchemas"]