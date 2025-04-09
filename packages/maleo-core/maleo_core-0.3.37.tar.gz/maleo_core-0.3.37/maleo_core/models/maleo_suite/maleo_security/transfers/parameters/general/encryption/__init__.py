# This file serves all MaleoSecurity's Encryption General Parameters

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralParameters

class MaleoSecurityEncryptionGeneralParameters:
    AES = MaleoSecurityAESEncryptionGeneralParameters

__all__ = [
    "MaleoSecurityEncryptionGeneralParameters",
    "MaleoSecurityAESEncryptionGeneralParameters"
]