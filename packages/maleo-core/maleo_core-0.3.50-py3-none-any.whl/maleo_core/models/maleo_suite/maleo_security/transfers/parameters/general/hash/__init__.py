# This file serves all MaleoSecurity's Hash General Parameters

from __future__ import annotations
from .hmac import MaleoSecurityHMACHashGeneralParameters
from .bcrypt import MaleoSecurityBcryptHashGeneralParameters
from .sha256 import MaleoSecuritySHA256HashGeneralParameters

class MaleoSecurityHashGeneralParameters:
    HMAC = MaleoSecurityHMACHashGeneralParameters
    Bcrypt = MaleoSecurityBcryptHashGeneralParameters
    SHA256 = MaleoSecuritySHA256HashGeneralParameters

__all__ = [
    "MaleoSecurityHashGeneralParameters",
    "MaleoSecurityHMACHashGeneralParameters",
    "MaleoSecurityBcryptHashGeneralParameters",
    "MaleoSecuritySHA256HashGeneralParameters"
]