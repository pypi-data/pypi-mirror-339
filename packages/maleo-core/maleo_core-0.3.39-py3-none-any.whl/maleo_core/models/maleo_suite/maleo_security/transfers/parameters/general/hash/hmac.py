from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityHMACHashGeneralParameters:
    class Hash(BaseModel):
        key:str = Field(..., description="HMAC Secret Key")
        message:str = Field(..., description="Message to be hashed")

    class Verify(MaleoSecurityHashGeneralTransfers.Base, Hash): pass