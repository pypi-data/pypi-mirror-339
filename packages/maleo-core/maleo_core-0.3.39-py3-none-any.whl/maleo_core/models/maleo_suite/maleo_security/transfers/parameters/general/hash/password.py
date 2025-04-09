from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityPasswordHashGeneralParameters:
    class Hash(BaseModel):
        password:str = Field(..., description="Password to be hashed")

    class Verify(MaleoSecurityHashGeneralTransfers.Base, Hash): pass