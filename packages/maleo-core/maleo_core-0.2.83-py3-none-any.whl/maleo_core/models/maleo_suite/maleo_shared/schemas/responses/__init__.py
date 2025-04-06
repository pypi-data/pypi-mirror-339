# This file serves all MaleoShared's responses schemas

from __future__ import annotations
from .services import MaleoSharedServicesResponsesSchemas

class MaleoSharedResponsesSchemas:
    Services = MaleoSharedServicesResponsesSchemas

__all__ = ["MaleoSharedResponsesSchemas", "MaleoSharedServicesResponsesSchemas"]