# This file serves all MaleoSecurity's General Parameters

from __future__ import annotations
from .key import MaleoSecurityKeyGeneralParameters
from .encryption import MaleoSecurityEncryptionGeneralParameters
from .hash import MaleoSecurityHashGeneralParameters
from .signature import MaleoSecuritySignatureGeneralParameters

class MaleoSecurityGeneralParameters:
    Key = MaleoSecurityKeyGeneralParameters
    Encryption = MaleoSecurityEncryptionGeneralParameters
    Hash = MaleoSecurityHashGeneralParameters
    Signature = MaleoSecuritySignatureGeneralParameters

__all__ = [
    "MaleoSecurityGeneralParameters",
    "MaleoSecurityKeyGeneralParameters",
    "MaleoSecurityEncryptionGeneralParameters",
    "MaleoSecurityHashGeneralParameters",
    "MaleoSecuritySignatureGeneralParameters"
]