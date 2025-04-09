# This file serves all MaleoSecurity's responses schemas

from __future__ import annotations
from .services import MaleoSecurityServicesResponsesSchemas

class MaleoSecurityResponsesSchemas:
    Services = MaleoSecurityServicesResponsesSchemas

__all__ = ["MaleoSecurityResponsesSchemas", "MaleoSecurityServicesResponsesSchemas"]