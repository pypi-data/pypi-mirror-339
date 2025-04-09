from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers

class MaleoSecurityHashGeneralResults:
    class IsValid(BaseModel):
        is_valid:bool = Field(..., description="Whether hash is valid")

    Fail = BaseGeneralResults.Fail

    class Hash(BaseGeneralResults.SingleData):
        data:MaleoSecurityHashGeneralTransfers.Hash

    class Verify(BaseGeneralResults.SingleData):
        data:MaleoSecurityHashGeneralResults.IsValid