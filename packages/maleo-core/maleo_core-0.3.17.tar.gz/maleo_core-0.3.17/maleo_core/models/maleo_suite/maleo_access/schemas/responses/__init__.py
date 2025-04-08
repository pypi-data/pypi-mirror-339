# This file serves all MaleoAccess's responses schemas

from __future__ import annotations
from .services import MaleoAccessServicesResponsesSchemas

class MaleoAccessResponsesSchemas:
    Services = MaleoAccessServicesResponsesSchemas

__all__ = ["MaleoAccessResponsesSchemas", "MaleoAccessServicesResponsesSchemas"]