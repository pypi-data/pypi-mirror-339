# This file serves all MaleoSecurity's Encryption General Transfers

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralTransfers
from .rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityEncryptionGeneralTransfers:
    AES = MaleoSecurityAESEncryptionGeneralTransfers
    RSA = MaleoSecurityRSAEncryptionGeneralTransfers

__all__ = [
    "MaleoSecurityEncryptionGeneralTransfers",
    "MaleoSecurityAESEncryptionGeneralTransfers",
    "MaleoSecurityRSAEncryptionGeneralTransfers"
]