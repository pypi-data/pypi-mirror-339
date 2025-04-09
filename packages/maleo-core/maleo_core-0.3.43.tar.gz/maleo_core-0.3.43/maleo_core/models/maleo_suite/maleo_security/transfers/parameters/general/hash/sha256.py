from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecuritySHA256HashGeneralParameters:
    class Hash(MaleoSecurityHashGeneralTransfers.Base): pass
    class Verify(MaleoSecurityHashGeneralTransfers.Hash, Hash): pass