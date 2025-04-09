# This file serves all MaleoSecurity's services responses schemas

from __future__ import annotations
from .secret import MaleoSecuritySecretServiceResponsesSchemas

class MaleoSecurityServicesResponsesSchemas:
    Secret = MaleoSecuritySecretServiceResponsesSchemas

__all__ = [
    "MaleoSecurityServicesResponsesSchemas",
    "MaleoSecuritySecretServiceResponsesSchemas"
]