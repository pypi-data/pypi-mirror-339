# This file serves all MaleoSecurity's General Transfers

from __future__ import annotations
from .secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecurityGeneralTransfers:
    Secret = MaleoSecuritySecretGeneralTransfers

__all__ = [
    "MaleoSecurityGeneralTransfers",
    "MaleoSecuritySecretGeneralTransfers"
]