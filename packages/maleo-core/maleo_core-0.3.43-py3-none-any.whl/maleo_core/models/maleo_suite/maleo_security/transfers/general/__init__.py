# This file serves all MaleoSecurity's General Transfers

from __future__ import annotations
from .secret import MaleoSecuritySecretGeneralTransfers
from .encryption import MaleoSecurityEncryptionGeneralTransfers
from .hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Secret = MaleoSecuritySecretGeneralTransfers
    Encryption = MaleoSecurityEncryptionGeneralTransfers
    Hash = MaleoSecurityHashGeneralTransfers

__all__ = [
    "MaleoSecurityGeneralTransfers",
    "MaleoSecuritySecretGeneralTransfers",
    "MaleoSecurityEncryptionGeneralTransfers",
    "MaleoSecurityHashGeneralTransfers"
]