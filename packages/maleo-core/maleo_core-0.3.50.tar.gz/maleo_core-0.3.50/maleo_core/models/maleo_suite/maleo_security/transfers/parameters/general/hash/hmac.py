from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityHMACHashGeneralParameters:
    class Base(BaseModel):
        key:str = Field(..., description="HMAC Secret Key")
    class Hash(MaleoSecurityHashGeneralTransfers.Base, Base): pass
    class Verify(MaleoSecurityHashGeneralTransfers.Hash, Hash): pass