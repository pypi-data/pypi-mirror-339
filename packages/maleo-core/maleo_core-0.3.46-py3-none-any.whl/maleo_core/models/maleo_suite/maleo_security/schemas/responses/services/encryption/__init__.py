# This file serves all MaleoSecurity's Encryption services responses schemas

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionServiceResponsesSchemas
from .rsa import MaleoSecurityRSAEncryptionServiceResponsesSchemas

class MaleoSecurityEncryptionServicesResponsesSchemas:
    AES = MaleoSecurityAESEncryptionServiceResponsesSchemas
    RSA = MaleoSecurityRSAEncryptionServiceResponsesSchemas

__all__ = [
    "MaleoSecurityEncryptionServicesResponsesSchemas",
    "MaleoSecurityAESEncryptionServiceResponsesSchemas",
    "MaleoSecurityRSAEncryptionServiceResponsesSchemas"
]