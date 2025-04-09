# This file serves all MaleoSecurity's AES Encryption General Results

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralResults
from .rsa import MaleoSecurityRSAEncryptionGeneralResults

class MaleoSecurityEncryptionGeneralResults:
    AES = MaleoSecurityAESEncryptionGeneralResults
    RSA = MaleoSecurityRSAEncryptionGeneralResults

__all__ = [
    "MaleoSecurityEncryptionGeneralResults",
    "MaleoSecurityAESEncryptionGeneralResults",
    "MaleoSecurityRSAEncryptionGeneralResults"
]