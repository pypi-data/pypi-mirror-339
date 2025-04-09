# This file serves all MaleoSecurity's General Parameters

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralParameters
from .encryption import MaleoSecurityEncryptionGeneralParameters

class MaleoSecurityGeneralParameters:
    Key = MaleoSecurityKeyGeneralParameters
    Encryption = MaleoSecurityEncryptionGeneralParameters

__all__ = [
    "MaleoSecurityGeneralParameters",
    "MaleoSecurityKeyGeneralParameters",
    "MaleoSecurityEncryptionGeneralParameters"
]