# This file serves all MaleoSecurity's General Transfers

from __future__ import annotations
from .secret import MaleoSecuritySecretGeneralTransfers
from .encryption import MaleoSecurityEncryptionGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Secret = MaleoSecuritySecretGeneralTransfers
    Encryption = MaleoSecurityEncryptionGeneralTransfers

__all__ = [
    "MaleoSecurityGeneralTransfers",
    "MaleoSecuritySecretGeneralTransfers",
    "MaleoSecurityEncryptionGeneralTransfers"
]