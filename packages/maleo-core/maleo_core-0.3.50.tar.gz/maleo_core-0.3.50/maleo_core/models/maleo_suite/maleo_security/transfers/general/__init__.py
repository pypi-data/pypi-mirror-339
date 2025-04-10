# This file serves all MaleoSecurity's General Transfers

from __future__ import annotations
from .secret import MaleoSecuritySecretGeneralTransfers
from .encryption import MaleoSecurityEncryptionGeneralTransfers
from .hash import MaleoSecurityHashGeneralTransfers
from .signature import MaleoSecuritySignatureGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Secret = MaleoSecuritySecretGeneralTransfers
    Encryption = MaleoSecurityEncryptionGeneralTransfers
    Hash = MaleoSecurityHashGeneralTransfers
    Signature = MaleoSecuritySignatureGeneralTransfers

__all__ = [
    "MaleoSecurityGeneralTransfers",
    "MaleoSecuritySecretGeneralTransfers",
    "MaleoSecurityEncryptionGeneralTransfers",
    "MaleoSecurityHashGeneralTransfers",
    "MaleoSecuritySignatureGeneralTransfers"
]