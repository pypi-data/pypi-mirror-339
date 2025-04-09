# This file serves all MaleoSecurity's services responses schemas

from __future__ import annotations
from .secret import MaleoSecuritySecretServiceResponsesSchemas
from .key import MaleoSecurityKeyServiceResponsesSchemas
from .encryption import MaleoSecurityEncryptionServicesResponsesSchemas

class MaleoSecurityServicesResponsesSchemas:
    Secret = MaleoSecuritySecretServiceResponsesSchemas
    Key = MaleoSecurityKeyServiceResponsesSchemas
    Encryption = MaleoSecurityEncryptionServicesResponsesSchemas

__all__ = [
    "MaleoSecurityServicesResponsesSchemas",
    "MaleoSecuritySecretServiceResponsesSchemas",
    "MaleoSecurityKeyServiceResponsesSchemas",
    "MaleoSecurityEncryptionServicesResponsesSchemas"
]