# This file serves all MaleoSecurity's General Results

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralResults
from .encryption import MaleoSecurityEncryptionGeneralResults
from .hash import MaleoSecurityHashGeneralResults
from .signature import MaleoSecuritySignatureGeneralResults

class MaleoSecurityGeneralResults:
    Key = MaleoSecurityKeyGeneralResults
    Encryption = MaleoSecurityEncryptionGeneralResults
    Hash = MaleoSecurityHashGeneralResults
    Signature = MaleoSecuritySignatureGeneralResults

__all__ = [
    "MaleoSecurityGeneralResults",
    "MaleoSecurityKeyGeneralResults",
    "MaleoSecurityEncryptionGeneralResults",
    "MaleoSecuritySignatureGeneralResults"
]