# This file serves all MaleoSecurity's Encryption General Parameters

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralParameters
from .rsa import MaleoSecurityRSAEncryptionGeneralParameters

class MaleoSecurityEncryptionGeneralParameters:
    AES = MaleoSecurityAESEncryptionGeneralParameters
    RSA = MaleoSecurityRSAEncryptionGeneralParameters

__all__ = [
    "MaleoSecurityEncryptionGeneralParameters",
    "MaleoSecurityAESEncryptionGeneralParameters",
    "MaleoSecurityRSAEncryptionGeneralParameters"
]