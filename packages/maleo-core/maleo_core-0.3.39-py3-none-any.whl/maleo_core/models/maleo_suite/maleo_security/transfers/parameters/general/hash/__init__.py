# This file serves all MaleoSecurity's Hash General Parameters

from __future__ import annotations
from .hmac import MaleoSecurityHMACHashGeneralParameters
from .password import MaleoSecurityPasswordHashGeneralParameters
from .sha256 import MaleoSecuritySHA256HashGeneralParameters

class MaleoSecurityHashGeneralParameters:
    HMAC = MaleoSecurityHMACHashGeneralParameters
    Password = MaleoSecurityPasswordHashGeneralParameters
    SHA256 = MaleoSecuritySHA256HashGeneralParameters

__all__ = [
    "MaleoSecurityHashGeneralParameters",
    "MaleoSecurityHMACHashGeneralParameters",
    "MaleoSecurityPasswordHashGeneralParameters",
    "MaleoSecuritySHA256HashGeneralParameters"
]