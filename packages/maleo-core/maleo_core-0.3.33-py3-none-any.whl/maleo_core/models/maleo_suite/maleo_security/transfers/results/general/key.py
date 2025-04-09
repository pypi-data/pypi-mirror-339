from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class MaleoSecurityKeyGeneralResults:
    class GeneratePrivate(BaseModel):
        private_key:str = Field(..., description="Private key in string")

    class GeneratePublic(BaseModel):
        public_key:str = Field(..., description="Public key in string")

    class GeneratePair(
        GeneratePublic,
        GeneratePrivate
    ): pass

    Fail = BaseGeneralResults.Fail

    class SinglePrivate(BaseGeneralResults.SingleData):
        data:MaleoSecurityKeyGeneralResults.GeneratePrivate

    class SinglePublic(BaseGeneralResults.SingleData):
        data:MaleoSecurityKeyGeneralResults.GeneratePublic

    class SinglePair(BaseGeneralResults.SingleData):
        data:MaleoSecurityKeyGeneralResults.GeneratePair