# This file serves all MaleoSecurity's Encryption General Transfers

from __future__ import annotations
from .aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityEncryptionGeneralTransfers:
    AES = MaleoSecurityAESEncryptionGeneralTransfers

__all__ = [
    "MaleoSecurityEncryptionGeneralTransfers",
    "MaleoSecurityAESEncryptionGeneralTransfers"
]