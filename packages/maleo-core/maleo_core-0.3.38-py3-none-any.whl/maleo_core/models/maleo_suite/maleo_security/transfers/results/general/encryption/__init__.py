# This file serves all MaleoSecurity's AES Encryption General Results

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralResults

class MaleoSecurityEncryptionGeneralResults:
    AES = MaleoSecurityAESEncryptionGeneralResults

__all__ = [
    "MaleoSecurityEncryptionGeneralResults",
    "MaleoSecurityAESEncryptionGeneralResults"
]