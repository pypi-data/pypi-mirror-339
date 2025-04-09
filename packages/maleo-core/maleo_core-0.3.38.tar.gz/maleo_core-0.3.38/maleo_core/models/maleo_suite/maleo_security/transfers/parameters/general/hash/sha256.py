from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecuritySHA256HashGeneralParameters:
    class Hash(BaseModel):
        message:str = Field(..., description="Message to be hashed")

    class Verify(MaleoSecurityHashGeneralTransfers.Base, Hash): pass