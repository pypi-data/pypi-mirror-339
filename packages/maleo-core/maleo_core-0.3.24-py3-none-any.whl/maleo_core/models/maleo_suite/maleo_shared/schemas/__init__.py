# This file serves all MaleoShared's Schemas

from __future__ import annotations
from .responses import MaleoSharedResponsesSchemas

class MaleoSharedSchemas:
    Responses = MaleoSharedResponsesSchemas

__all__ = ["MaleoSharedSchemas", "MaleoSharedResponsesSchemas"]