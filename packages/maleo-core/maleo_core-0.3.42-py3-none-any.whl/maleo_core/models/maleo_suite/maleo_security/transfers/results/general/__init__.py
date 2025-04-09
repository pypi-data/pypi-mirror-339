# This file serves all MaleoSecurity's General Results

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralResults
from .encryption import MaleoSecurityEncryptionGeneralResults

class MaleoSecurityGeneralResults:
    Key = MaleoSecurityKeyGeneralResults
    Encryption = MaleoSecurityEncryptionGeneralResults

__all__ = [
    "MaleoSecurityGeneralResults",
    "MaleoSecurityKeyGeneralResults",
    "MaleoSecurityEncryptionGeneralResults"
]