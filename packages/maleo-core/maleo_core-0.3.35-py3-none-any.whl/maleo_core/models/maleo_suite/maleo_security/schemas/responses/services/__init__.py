# This file serves all MaleoSecurity's services responses schemas

from __future__ import annotations
from .secret import MaleoSecuritySecretServiceResponsesSchemas
from .key import MaleoSecurityKeyServiceResponsesSchemas

class MaleoSecurityServicesResponsesSchemas:
    Secret = MaleoSecuritySecretServiceResponsesSchemas
    Key = MaleoSecurityKeyServiceResponsesSchemas

__all__ = [
    "MaleoSecurityServicesResponsesSchemas",
    "MaleoSecuritySecretServiceResponsesSchemas",
    "MaleoSecurityKeyServiceResponsesSchemas"
]