# This file serves all MaleoSecurity's Encryption services responses schemas

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionServiceResponsesSchemas

class MaleoSecurityEncryptionServicesResponsesSchemas:
    AES = MaleoSecurityAESEncryptionServiceResponsesSchemas

__all__ = [
    "MaleoSecurityEncryptionServicesResponsesSchemas",
    "MaleoSecurityAESEncryptionServiceResponsesSchemas",
]