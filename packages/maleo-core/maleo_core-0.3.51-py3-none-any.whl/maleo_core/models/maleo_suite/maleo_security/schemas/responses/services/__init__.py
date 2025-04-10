# This file serves all MaleoSecurity's services responses schemas

from __future__ import annotations
from .secret import MaleoSecuritySecretServiceResponsesSchemas
from .key import MaleoSecurityKeyServiceResponsesSchemas
from .encryption import MaleoSecurityEncryptionServicesResponsesSchemas
from .hash import MaleoSecurityHashServiceResponsesSchemas
from .signature import MaleoSecuritySignatureServiceResponsesSchemas

class MaleoSecurityServicesResponsesSchemas:
    Secret = MaleoSecuritySecretServiceResponsesSchemas
    Key = MaleoSecurityKeyServiceResponsesSchemas
    Encryption = MaleoSecurityEncryptionServicesResponsesSchemas
    Hash = MaleoSecurityHashServiceResponsesSchemas
    Signature = MaleoSecuritySignatureServiceResponsesSchemas

__all__ = [
    "MaleoSecurityServicesResponsesSchemas",
    "MaleoSecuritySecretServiceResponsesSchemas",
    "MaleoSecurityKeyServiceResponsesSchemas",
    "MaleoSecurityEncryptionServicesResponsesSchemas",
    "MaleoSecurityHashServiceResponsesSchemas",
    "MaleoSecuritySignatureServiceResponsesSchemas"
]