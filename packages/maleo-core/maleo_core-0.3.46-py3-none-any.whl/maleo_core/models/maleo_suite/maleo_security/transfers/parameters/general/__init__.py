# This file serves all MaleoSecurity's General Parameters

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralParameters
from .encryption import MaleoSecurityEncryptionGeneralParameters
from .hash import MaleoSecurityHashGeneralParameters

class MaleoSecurityGeneralParameters:
    Key = MaleoSecurityKeyGeneralParameters
    Encryption = MaleoSecurityEncryptionGeneralParameters
    Hash = MaleoSecurityHashGeneralParameters

__all__ = [
    "MaleoSecurityGeneralParameters",
    "MaleoSecurityKeyGeneralParameters",
    "MaleoSecurityEncryptionGeneralParameters",
    "MaleoSecurityHashGeneralParameters"
]